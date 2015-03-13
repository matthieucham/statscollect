from django.test import TestCase
from statscollect_scrap import scrappers


class FootballStepScrapper(TestCase):

    def test_LFP_scrapper(self):
        my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=28&id=0'
        scrapper = scrappers.LFPFootballStepScrapper()
        scrapper.scrap(my_url)
        self.assertTrue(True)

