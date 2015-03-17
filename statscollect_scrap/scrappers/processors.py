import importlib
from fuzzywuzzy import process
from statscollect_db.models import FootballTeam, TournamentInstance, TournamentInstanceStep


class FootballMeetingProcessingResult():
    def __init__(self, game):
        self.scrapped_game = game
        self.matching_home_team = None
        self.matching_home_ratio = 0.0
        self.matching_away_team = None
        self.matching_away_ratio = 0.0


class FootballStepProcessor():
    CUTOFF_PREFERRED = 50
    CUTOFF_SECONDARY = 90

    # Ensemble de recherche.
    choices_preferred = dict([(elem['id'], elem['name']) for elem in FootballTeam.objects.all().values('id', 'name')])
    choices_secondary = dict([(elem['id'], elem['short_name']) for elem in FootballTeam.objects.all().values('id',
                                                                                                             'short_name')])

    def __init__(self, step=None, step_name=None):
        self.processed_step = step
        self.step_name = step_name

    def process(self, url, scrapper_class_name):
        module = importlib.import_module('statscollect_scrap.scrappers.football_step_scrappers')
        klass = getattr(module, scrapper_class_name)
        scrapper = klass()
        results = self.scrap_and_match(url, scrapper)
        return results



    def scrap_and_match(self, scrap_url, scrapper):
        step_games = scrapper.scrap(scrap_url)

        matching_results = []

        for game in step_games:
            matching_results.append(self.process_game(game))

        return matching_results

    def process_game(self, game_pivot):

        process_result = FootballMeetingProcessingResult(game_pivot)

        # Search Home
        found_id, ratio = self.search_team(game_pivot.home_team_name)
        if found_id is not None:
            process_result.matching_home_team = found_id
            process_result.matching_home_ratio = ratio

        # Search Away
        found_id, ratio = self.search_team(game_pivot.away_team_name)
        if found_id is not None:
            process_result.matching_away_team = found_id
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
            return team_id, ratio
        else:
            print("Alert : no match for %s" % team_name)
            return None, 0.0
