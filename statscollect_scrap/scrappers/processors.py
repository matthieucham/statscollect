import importlib
from fuzzywuzzy import process
from statscollect_db.models import FootballTeam, FootballPerson, TeamMeetingPerson
from statscollect_scrap import models


def search_player(player_name, choices, cutoff):
    print('Searching %s' % player_name)
    matching_results = process.extractBests(player_name, choices,
                                            score_cutoff=cutoff,
                                            limit=1)
    if len(matching_results) > 0:
        result, ratio, player_id = matching_results[0]
        print('Found %s with ratio %s' % (result, ratio))
        matching_player = FootballPerson.objects.get(pk=player_id)
        return matching_player, ratio
    else:
        print("Alert : no match for %s" % player_name)
        return None, 0.0


class BaseProcessor():
    def process(self, url, scrapper_class_name):
        module = importlib.import_module('statscollect_scrap.scrappers.scrappers')
        klass = getattr(module, scrapper_class_name)
        scrapper = klass()
        results = self.scrap_and_match(url, scrapper)
        return results

    def scrap_and_match(self, scrap_url, scrapper):
        raise NotImplementedError

    def create_target_object(self):
        raise NotImplementedError


class FootballStepProcessor(BaseProcessor):
    CUTOFF_PREFERRED = 80
    CUTOFF_SECONDARY = 80

    # Ensemble de recherche.
    choices_preferred = dict([(elem['id'], elem['name']) for elem in FootballTeam.objects.all().values('id', 'name')])
    choices_secondary = dict([(elem['id'], elem['short_name']) for elem in FootballTeam.objects.all().values('id',
                                                                                                             'short_name')])

    def __init__(self, parent_entity):
        self.parent_entity = parent_entity
        self.processed_step = parent_entity.actual_step

    def scrap_and_match(self, scrap_url, scrapper):
        step_games = scrapper.scrap(scrap_url)
        matching_results = []
        for game in step_games:
            game['fk_scrapped_step'] = self.parent_entity
            matching_results.append(self.process_game(game))
        return matching_results

    def process_game(self, game):
        # process_result = FootballMeetingProcessingResult(game_pivot)
        for field in ['home', 'away']:
            found, ratio = self.search_team(game['read_%s_team' % field])
            if found is not None:
                game['actual_%s_team' % field] = found
            game['ratio_%s_team' % field] = ratio
        return game

    def search_team(self, team_name):
        print('Searching %s' % team_name)
        matching_results = process.extractBests(team_name, FootballStepProcessor.choices_preferred,
                                                score_cutoff=FootballStepProcessor.CUTOFF_PREFERRED,
                                                limit=1)
        if len(matching_results) == 0:
            # search again with secondary choices this time.
            matching_results = process.extractBests(team_name,
                                                    FootballStepProcessor.choices_secondary,
                                                    score_cutoff=FootballStepProcessor.CUTOFF_SECONDARY,
                                                    limit=1)
        if len(matching_results) > 0:
            home_result, ratio, team_id = matching_results[0]
            print('Found %s with ratio %s' % (home_result, ratio))
            matching_team = FootballTeam.objects.get(pk=team_id)
            return matching_team, ratio
        else:
            print("Alert : no match for %s" % team_name)
            return None, 0.0

    def create_target_object(self):
        obj = models.ScrappedFootballGameResult()
        obj.scrapped_game_sheet = self.parent_entity
        return obj


class FootballGamesheetProcessor(BaseProcessor):
    CUTOFF_PREFERRED = 70

    def __init__(self, parent_entity):
        self.parent_entity = parent_entity
        self.home_team = parent_entity.actual_meeting.home_team
        self.away_team = parent_entity.actual_meeting.away_team
        self.choices_home = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(current_teams=self.home_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )
        self.choices_away = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(current_teams=self.away_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )

    def scrap_and_match(self, scrap_url, scrapper):
        scrapped_players = scrapper.scrap(scrap_url)
        matching_results = []
        for player in scrapped_players:
            matching_results.append(self.process_player(player))
        return matching_results

    def process_player(self, player):
        # Search Home
        is_home = player.pop('is_home')
        if is_home:
            found, ratio = search_player(player['read_player'], self.choices_home,
                                         FootballGamesheetProcessor.CUTOFF_PREFERRED)
        else:
            found, ratio = search_player(player['read_player'], self.choices_away,
                                         FootballGamesheetProcessor.CUTOFF_PREFERRED)
        if found is not None:
            player['fk_actual_player'] = found
            player['fk_ratio_player'] = ratio
        player['fk_actual_team'] = self.home_team if is_home else self.away_team
        return player

    def create_target_object(self):
        obj = models.ScrappedGameSheetParticipant()
        obj.scrapped_game_sheet = self.parent_entity
        return obj


class FootballStatsProcessor(BaseProcessor):
    # cutoff faible car la sélection a été déjà faite avant
    CUTOFF_PREFERRED = 40

    def __init__(self, parent_entity):
        self.parent_entity = parent_entity
        self.choices_home = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=parent_entity.teammeeting,
                                                       teammeetingperson__played_for=parent_entity.teammeeting.home_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )
        self.choices_away = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=parent_entity.teammeeting,
                                                       teammeetingperson__played_for=parent_entity.teammeeting.away_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )

    def scrap_and_match(self, scrap_url, scrapper):
        stats = scrapper.scrap(scrap_url)
        matching_results = []
        for statline in stats:
            matching_results.append(self.process_stats(statline))
        return matching_results

    def process_stats(self, statline):
        player_name = statline.pop('read_player')
        if statline.pop('team') == 'home':
            found, ratio = search_player(player_name, self.choices_home,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        else:
            found, ratio = search_player(player_name, self.choices_away,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        if found is not None:
            statline['fk_teammeetingperson'] = TeamMeetingPerson.objects.get(person=found,
                                                                             meeting=self.parent_entity.teammeeting)
        else:
            raise ValueError('No matching player found for name %s : fix registered playered in the gamesheet then '
                             'process again' % player_name)
        return statline

    def create_target_object(self):
        obj = models.ScrappedPlayerStats()
        obj.teammeeting = self.parent_entity
        return obj


class FootballRatingsProcessor(BaseProcessor):
    # cutoff faible car la sélection a été déjà faite avant
    CUTOFF_PREFERRED = 40

    def __init__(self, parent_entity):
        self.parent_entity = parent_entity
        self.choices_home = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=parent_entity.teammeeting,
                                                       teammeetingperson__played_for=parent_entity.teammeeting.home_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )
        self.choices_away = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=parent_entity.teammeeting,
                                                       teammeetingperson__played_for=parent_entity.teammeeting.away_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )

    def create_target_object(self):
        obj = models.ScrappedPlayerRatings()
        obj.scrapped_meeting = self.parent_entity
        return obj

    def scrap_and_match(self, scrap_url, scrapper):
        ratings = scrapper.scrap(scrap_url)
        matching_results = []
        for rating in ratings:
            matching_results.append(self.process_rating(rating))
        return matching_results

    def process_rating(self, rating):
        player_name = rating.pop('read_player')
        if rating.pop('team') == 'home':
            found, ratio = search_player(player_name, self.choices_home,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        else:
            found, ratio = search_player(player_name, self.choices_away,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        if found is not None:
            rating['fk_teammeetingperson'] = TeamMeetingPerson.objects.get(person=found,
                                                                           meeting=self.parent_entity.teammeeting)
        else:
            raise ValueError('No matching player found for name %s : fix registered playered in the gamesheet then '
                             'process again' % player_name)
        return rating