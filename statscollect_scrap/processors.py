__author__ = 'Matt'
import dateutil.parser
from fuzzywuzzy import process, fuzz
from statscollect_scrap import models
from statscollect_scrap.scrappers import myfuzz
from statscollect_db.models import FootballTeam, FootballPerson


class GamesheetProcessor():
    # Ensemble de recherche.
    team_choices_preferred = dict(
        [(elem['id'], elem['name']) for elem in FootballTeam.objects.all().values('id', 'name')])
    team_choices_secondary = dict([(elem['id'], elem['short_name']) for elem in FootballTeam.objects.all().values('id',
                                                                                                                  'short_name')])

    def process(self, processedgame):
        summary = self.process_summary(processedgame.gamesheet_ds.content)
        if not (summary.home_team and summary.away_team):
            raise ValueError("Could not scrap GameSummary: teams not matched")
        # delete previous if any:
        models.ProcessedGameSummary.objects.filter(processed_game=processedgame).delete()
        # set the new one
        summary.processed_game = processedgame
        summary.save()

        players = self.process_players(processedgame.gamesheet_ds.content,
                                       teams={'home': summary.home_team, 'away': summary.away_team})
        # delete previous if any:
        models.ProcessedGameSheetPlayer.objects.filter(processed_game=processedgame).delete()
        # register scraped players
        for pl in players:
            pl.processed_game = processedgame
            pl.save()

        processedgame.status = 'PENDING'
        processedgame.save()

    def process_players(self, data, teams):
        for key in ['home', 'away']:
            choices = dict(
                [(elem['id'], elem['first_name'][:3] + ' ' + elem['last_name'] + ' ' + elem['usual_name'])
                 for elem in
                 FootballPerson.objects.filter(current_teams=teams[key]).values('id', 'first_name', 'last_name',
                                                                                'usual_name')]
            )
            for pl in data['players_'+key]:
                teammeetingperson, ratio = self.find_person(pl['name'], choices)
                stats = pl.get('stats', {})
                yield models.ProcessedGameSheetPlayer(scraped_name=pl['name'], scraped_ratio=ratio,
                                                      footballperson=teammeetingperson,
                                                      playtime=int(stats.get('playtime', 0)),
                                                      goals_scored=int(stats.get('goals_scored', 0)),
                                                      penalties_scored=int(stats.get('penalties_scored', 0)),
                                                      goals_assists=int(stats.get('goals_assists', 0)),
                                                      penalties_assists=int(stats.get('penalties_assists', 0)),
                                                      goals_saves=int(stats.get('goals_saves', 0)),
                                                      goals_conceded=int(stats.get('goals_conceded', 0)),
                                                      own_goals=int(stats.get('own_goals', 0)),
                )

    def process_summary(self, data):
        home_team, away_team = self.find_teams(data)
        home_score, away_score = int(data['home_score']), int(data['away_score'])
        match_date = dateutil.parser.parse(data['match_date'])
        return models.ProcessedGameSummary(home_team=home_team, away_team=away_team, home_score=home_score,
                                           away_score=away_score, game_date=match_date)

    def find_person(self, player_name, choices):
        print('Searching %s' % player_name)
        matching_results = process.extractBests(player_name, choices,
                                                scorer=fuzz.partial_token_set_ratio,
                                                score_cutoff=0)
        if len(matching_results) > 0:
            # si les meilleurs matchs sont à egalité de score, chercher à nouveau avec méthode différente
            best_score = 0
            creme = dict()
            for name, score, plid in matching_results:
                if score >= best_score:
                    best_score = score
                    creme.update({plid: name})
                else:
                    # la liste renvoyée par extractBests est triée donc on peut s'arreter dès que le niveau baisse.
                    break
            # combien de meilleurs scores ?
            if len(creme) == 1:
                plid, plname = creme.popitem()
                print('Found %s at first round with ratio %s' % (plname, best_score))
                matching_player = FootballPerson.objects.get(pk=plid)
                return matching_player, best_score
            else:
                print('Multiple matches found with ratio %s, refining...' % best_score)
                refine_results = process.extractBests(player_name, creme,
                                                      scorer=myfuzz.partial_token_set_ratio_with_avg)
                plname, ratio, plid = refine_results[0]
                print('Found %s at second round with ratio %s then %s' % (plname, best_score, ratio))
                matching_player = FootballPerson.objects.get(pk=plid)
                return matching_player, best_score
        else:
            print("Alert : no match for %s" % player_name)
            return None, 0.0

    def find_teams(self, datasheet):
        ht = self.search_team(datasheet['home_team'])
        at = self.search_team(datasheet['away_team'])
        return ht, at

    def search_team(self, team_name):
        ratio_limit = 80
        print('Searching %s' % team_name)
        matching_results = process.extractBests(team_name, self.team_choices_preferred,
                                                scorer=fuzz.partial_ratio,
                                                score_cutoff=80,
                                                limit=1)
        if len(matching_results) == 0:
            # search again with secondary choices this time.
            matching_results = process.extractBests(team_name,
                                                    self.team_choices_secondary,
                                                    scorer=fuzz.partial_ratio,
                                                    score_cutoff=80,
                                                    limit=1)
        if len(matching_results) > 0:
            home_result, ratio, team_id = matching_results[0]
            print('Found %s with ratio %d - limit is %d' % (home_result, ratio, ratio_limit))
            if ratio >= ratio_limit:
                matching_team = FootballTeam.objects.get(pk=team_id)
                return matching_team
        print("Alert : no valid match for %s" % team_name)
        return None
