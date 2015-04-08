from django.test import TestCase
from statscollect_scrap import scrappers
from statscollect_db.models import FootballMeeting


class TestFootballScrapper(TestCase):
    def test_LFP_scrapper(self):
        my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=26&id=0'
        scrapper = scrappers.LFPFootballStepScrapper()
        scrapper.scrap(my_url)
        self.assertTrue(True)

    def test_LEquipe_scrapper(self):
        my_url = 'http://www.lequipe.fr/Football/FootballResultat48016.html'
        scrapper = scrappers.LEquipeFootballStepScrapper()
        scrapper.scrap(my_url)
        self.assertTrue(True)

    def test_Fuzzy(self):
        # my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=28
        # &id=0'
        my_url = 'http://www.lequipe.fr/Football/FootballResultat48019.html'
        # scrapper = 'LFPFootballStepScrapper'
        scrapper = 'LEquipeFootballStepScrapper'
        results = scrappers.FootballStepProcessor().process(my_url, scrapper)
        self.assertTrue(len(results) == 10)
        for res in results:
            self.assertTrue(res.matching_home_team is not None)

    def test_LFPGamesheet(self):
        my_url = 'http://www.lfp.fr/ligue1/feuille_match/showInfosMatch?matchId=79075&domId=35&extId=283&live=0&domNomClub=Paris+Saint-Germain&extNomClub=FC+Lorient'
        scrapper = scrappers.LFPFootballGamesheetScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) == 26)

    def test_WhoscoreGamesheet(self):
        my_url = 'http://www.whoscored.com/Matches/824607/Live'
        scrapper = scrappers.WhoscoredFGSScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) == 26)

    def test_Fuzzy_Player(self):
        my_url = 'http://www.whoscored.com/Matches/824471/Live'
        scrapper = 'WhoscoredFootballGamesheetScrapper'
        results = scrappers.FootballGamesheetProcessor(
            FootballMeeting.objects.get(uuid='3d6b176a-7125-48cc-bf7c-7182aee12db2')).process(my_url, scrapper)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print("%s matched by %s" % (res.participant.read_player, res.matching_player))

    def test_Fuzzy_Player2(self):
        my_url = 'http://www.lfp.fr/ligue1/feuille_match/showInfosMatch?matchId=79047&domId=35&extId=283&live=0' \
                 '&domNomClub=Paris+Saint-Germain&extNomClub=FC+Lorient'
        scrapper = 'LFPFootballGamesheetScrapper'
        results = scrappers.FootballGamesheetProcessor(
            FootballMeeting.objects.get(uuid='3d6b176a-7125-48cc-bf7c-7182aee12db2')).process(my_url, scrapper)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print("%s matched by %s" % (res.participant.read_player, res.matching_player))

    def test_WhoscoredStats(self):
        my_url = 'http://www.whoscored.com/Matches/824572/Live'
        scrapper = scrappers.WhoscoredStatsScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    def test_processor_stats(self):
        my_url = 'http://www.whoscored.com/Matches/824582/Live'
        scrapper = 'WhoscoredStatsScrapper'
        results = scrappers.FootballStatsProcessor(
            FootballMeeting.objects.get(uuid='05a76fb2-0ece-4fe0-829f-ddecebd4f154')).process(my_url, scrapper)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    def test_OrangeNotes(self):
        my_url = 'http://sports.orange.fr/football/compte-rendu/ligue-1/marseille-caen.html'
        scrapper = scrappers.OrangeRatingsScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) == 22)
        for res in results:
            print(res)

    def test_WhoscoredNotes(self):
        my_url = 'http://www.whoscored.com/Matches/824572/Live'
        scrapper = scrappers.WhoscoredRatingsScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) == 28)
        for res in results:
            print(res)