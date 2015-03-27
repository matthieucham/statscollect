from django.test import TestCase
from statscollect_scrap import scrappers


class FootballStepScrapper(TestCase):

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
        #my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=28
        # &id=0'
        my_url = 'http://www.lequipe.fr/Football/FootballResultat48019.html'
        #scrapper = 'LFPFootballStepScrapper'
        scrapper = 'LEquipeFootballStepScrapper'
        results = scrappers.FootballStepProcessor().process(my_url, scrapper)
        self.assertTrue(len(results) == 10)
        for res in results:
            self.assertTrue(res.matching_home_team is not None)

