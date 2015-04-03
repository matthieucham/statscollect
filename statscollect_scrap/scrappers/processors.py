import importlib
from fuzzywuzzy import process
from statscollect_db.models import FootballTeam, FootballPerson


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


class FootballMeetingProcessingResult():
    def __init__(self, game):
        self.scrapped_game = game
        self.matching_home_team = None
        self.matching_home_ratio = 0.0
        self.matching_away_team = None
        self.matching_away_ratio = 0.0


class FootballStepProcessor(BaseProcessor):
    CUTOFF_PREFERRED = 70
    CUTOFF_SECONDARY = 90

    # Ensemble de recherche.
    choices_preferred = dict([(elem['id'], elem['name']) for elem in FootballTeam.objects.all().values('id', 'name')])
    choices_secondary = dict([(elem['id'], elem['short_name']) for elem in FootballTeam.objects.all().values('id',
                                                                                                             'short_name')])

    def __init__(self, step=None, step_name=None):
        self.processed_step = step
        self.step_name = step_name

    def scrap_and_match(self, scrap_url, scrapper):
        step_games = scrapper.scrap(scrap_url)
        matching_results = []
        for game in step_games:
            matching_results.append(self.process_game(game))
        return matching_results

    def process_game(self, game_pivot):
        process_result = FootballMeetingProcessingResult(game_pivot)
        # Search Home
        found, ratio = self.search_team(game_pivot.home_team_name)
        if found is not None:
            process_result.matching_home_team = found
            process_result.matching_home_ratio = ratio
        # Search Away
        found, ratio = self.search_team(game_pivot.away_team_name)
        if found is not None:
            process_result.matching_away_team = found
            process_result.matching_away_ratio = ratio
        return process_result

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


class FootballGamesheetParticipantProcessingResult():
    def __init__(self, scrapped):
        self.participant = scrapped
        self.matching_player = None
        self.matching_ratio = 0.0
        self.matching_player_team = None


class FootballGamesheetProcessor(BaseProcessor):
    CUTOFF_PREFERRED = 70

    def __init__(self, team_meeting):
        self.home_team = team_meeting.home_team
        self.away_team = team_meeting.away_team
        self.choices_home = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(current_teams=team_meeting.home_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )
        self.choices_away = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(current_teams=team_meeting.away_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )

    def scrap_and_match(self, scrap_url, scrapper):
        scrapped_players = scrapper.scrap(scrap_url)
        matching_results = []
        for player in scrapped_players:
            matching_results.append(self.process_player(player))
        return matching_results

    def process_player(self, player):
        process_result = FootballGamesheetParticipantProcessingResult(player)
        # Search Home
        if player.is_home:
            found, ratio = search_player(player.read_player, self.choices_home,
                                         FootballGamesheetProcessor.CUTOFF_PREFERRED)
        else:
            found, ratio = search_player(player.read_player, self.choices_away,
                                         FootballGamesheetProcessor.CUTOFF_PREFERRED)
        if found is not None:
            process_result.matching_player = found
            process_result.matching_ratio = ratio
        process_result.matching_player_team = self.home_team if player.is_home else self.away_team
        return process_result


class FootballStatsProcessor(BaseProcessor):
    # cutoff faible car la sélection a été déjà faite avant
    CUTOFF_PREFERRED = 40

    def __init__(self, team_meeting):
        self.choices_home = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=team_meeting,
                                                       teammeetingperson__played_for=team_meeting.home_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )
        self.choices_away = dict(
            [(elem['id'], elem['first_name'] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
             for elem in FootballPerson.objects.filter(teammeetingperson__meeting=team_meeting,
                                                       teammeetingperson__played_for=team_meeting.away_team).values(
                'id', 'first_name', 'last_name', 'usual_name')]
        )

    def scrap_and_match(self, scrap_url, scrapper):
        stats = scrapper.scrap(scrap_url)
        matching_results = []
        for statline in stats:
            matching_results.append(self.process_stats(statline))
        return matching_results

    def process_stats(self, statline):
        process_result = dict(statline)
        # Search Home
        if statline['team'] == 'home':
            found, ratio = search_player(statline['read_player'], self.choices_home,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        else:
            found, ratio = search_player(statline['read_player'], self.choices_away,
                                         FootballStatsProcessor.CUTOFF_PREFERRED)
        if found is not None:
            process_result['actual_player'] = found
            process_result['ratio_player'] = ratio
        else:
            raise ValueError('No matching player found for name %s : fix registered playered in the gamesheet then '
                             'process again' % statline['read_player'])
        return process_result
