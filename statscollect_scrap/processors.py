__author__ = 'Matt'
import dateutil.parser

from fuzzywuzzy import process

from statscollect_scrap import models

from statscollect_db.models import FootballTeam


class GamesheetProcessor():
    # Ensemble de recherche.
    team_choices_preferred = dict(
        [(elem['id'], elem['name']) for elem in FootballTeam.objects.all().values('id', 'name')])
    team_choices_secondary = dict([(elem['id'], elem['short_name']) for elem in FootballTeam.objects.all().values('id',
                                                                                                                  'short_name')])

    def process(self, processedgame):
        summary = self.process_summary(processedgame.gamesheet_ds.content)
        # delete previous if any:
        models.ProcessedGameSummary.objects.filter(processed_game=processedgame).delete()
        # set the new one
        summary.processed_game = processedgame
        summary.save()

    def process_summary(self, data):
        home_team, away_team = self.find_teams(data)
        home_score, away_score = int(data['home_score']), int(data['away_score'])
        match_date = dateutil.parser.parse(data['match_date'])
        return models.ProcessedGameSummary(home_team=home_team, away_team=away_team, home_score=home_score,
                                           away_score=away_score, game_date=match_date)

    def find_teams(self, datasheet):
        ht, _ = self.search_team(datasheet['home_team'])
        at, _ = self.search_team(datasheet['away_team'])
        return ht, at

    def search_team(self, team_name):
        print('Searching %s' % team_name)
        matching_results = process.extractBests(team_name, self.team_choices_preferred,
                                                score_cutoff=80,
                                                limit=1)
        if len(matching_results) == 0:
            # search again with secondary choices this time.
            matching_results = process.extractBests(team_name,
                                                    self.team_choices_secondary,
                                                    score_cutoff=80,
                                                    limit=1)
        if len(matching_results) > 0:
            home_result, ratio, team_id = matching_results[0]
            print('Found %s with ratio %s' % (home_result, ratio))
            matching_team = FootballTeam.objects.get(pk=team_id)
            return matching_team, ratio
        else:
            print("Alert : no match for %s" % team_name)
            return None, 0.0

