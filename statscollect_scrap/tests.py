from django.test import TestCase
from statscollect_scrap import scrappers
from statscollect_db.models import FootballMeeting, TournamentInstanceStep
from statscollect_scrap import models


class TestFootballScrapper(TestCase):
    def test_LFP_scrapper(self):
        my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=32&id=0'
        scrapper = scrappers.LFPFootballStepScrapper()
        scrapper.scrap(my_url)
        self.assertTrue(True)

    def test_LEquipe_scrapper(self):
        my_url = 'http://www.lequipe.fr/Football/Euro/Saison-2016/calendrier-resultats.html'
        scrapper = scrappers.LEquipeFootballStepScrapper()
        accessor = scrappers.URLAccessor(scrapper.url_pattern, '')
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url}
        results = scrapper.scrap_page(accessor.get_content(form))
        self.assertTrue(True)

    def test_UEFA_scrapper(self):
        my_url = 'http://fr.euro2016.infra.uefa.com/matches/libraries/1/matches'
        scrapper = scrappers.UEFAStepScrapper()
        accessor = scrappers.URLAccessor(scrapper.url_pattern, '')
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url}
        results = scrapper.scrap_page(accessor.get_content(form))
        for res in results:
            print(res)
        self.assertTrue(True)

    def test_Fuzzy(self):
        my_url = 'http://www.lfp.fr/competitionPluginCalendrierResultat/changeCalendrierHomeJournee?c=ligue1&js=28'
        # my_url = 'http://www.lequipe.fr/Football/FootballResultat48019.html'
        scrapper = 'LFPFootballStepScrapper'
        # scrapper = 'LEquipeFootballStepScrapper'
        step = models.ScrappedFootballStep()
        step.actual_step = TournamentInstanceStep()
        results = scrappers.FootballStepProcessor(step).process(my_url, scrapper)
        self.assertTrue(len(results) == 10)
        for res in results:
            print(res)

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
        my_url = 'http://www.whoscored.com/Matches/960846/Live'
        scrapper = scrappers.WhoscoredStatsScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    def test_processor_stats(self):
        my_url = 'http://www.whoscored.com/Matches/824511/Live'
        scrapper = 'WhoscoredStatsScrapper'
        results = scrappers.FootballStatsProcessor(
            FootballMeeting.objects.get(uuid='51167adc-f597-4f6c-b06c-6784b50cec2b')).process(my_url, scrapper)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    class TestForm(object):
        cleaned_data = {}

    class TestScrapperData(object):
        url_pattern = ''
        class_name = ''


    def test_OrangeNotes(self):
        my_url = 'http://sports.orange.fr/football/ligue-1/match/psg-nice-apres-match-SPEF010amU0iNC.html'
        scrapper = scrappers.OrangeRatingsScrapper()
        accessor = scrappers.URLAccessor(scrapper.url_pattern, '')
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url}
        results = scrapper.scrap_page(accessor.get_content(form))
        for res in results:
            print(res)

    def test_WhoscoredNotes(self):
        my_url = 'http://www.whoscored.com/Matches/824572/Live'
        scrapper = scrappers.WhoscoredRatingsScrapper()
        results = scrapper.scrap(my_url)
        self.assertTrue(len(results) == 28)
        for res in results:
            print(res)

    def test_OrangeNotesReverseTeams(self):
        my_url = 'http://sports.orange.fr/football/compte-rendu/ligue-1/montpellier-lyon.html'
        scrapper = 'OrangeRatingsScrapper'
        results = scrappers.FootballRatingsProcessor(
            FootballMeeting.objects.get(uuid='9ede93c2-41b9-49a9-943e-d44c764ea081')).process(my_url, scrapper)
        self.assertTrue(len(results) == 22)
        for res in results:
            print(res)

    def test_SportsNotes(self):
        my_url = 'http://www.sports.fr/football/compte-rendu/ligue-1/marseille-lyon.html'
        scrapper = scrappers.SportsFrRatingsScrapper()
        accessor = scrappers.URLAccessor(scrapper.url_pattern, '')
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url}
        results = scrapper.scrap_page(accessor.get_content(form))
        self.assertTrue(len(results) == 22)
        for res in results:
            print(res)

    def test_processor_notes(self):
        my_url = 'http://sports.orange.fr/football/ligue-1/match/monaco-bordeaux-apres-match-SPEF010amU0iNw.html'
        scrapper_data = TestFootballScrapper.TestScrapperData()
        scrapper_data.class_name = 'OrangeRatingsScrapper'
        scrapper_data.url_pattern = 'http\:\/\/sports\.orange\.fr\/football\/ligue\-1\/match\/(.*).html'
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url, 'mode': 'URL'}
        results = scrappers.FootballRatingsProcessor(
            FootballMeeting.objects.get(uuid='3173b9c6-3913-430c-837f-2cba567a9c50')).process(form, scrapper_data)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    def test_KickerNotes(self):
        my_url = 'http://www.kicker.de/news/fussball/em/spielplan/europameisterschaft/2016/1/2394895/spielanalyse_frankreich_rumaenien.html'
        scrapper = scrappers.KickerRatingsScrapper()
        accessor = scrappers.URLAccessor(scrapper.url_pattern, '')
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url}
        results = scrapper.scrap_page(accessor.get_content(form))
        self.assertTrue(len(results) == 22)
        for res in results:
            print(res)

    def test_processor_notes_kicker(self):
        my_url = 'http://www.kicker.de/news/fussball/em/spielplan/europameisterschaft/2016/1/2394895/spielanalyse_frankreich_rumaenien.html'
        scrapper_data = TestFootballScrapper.TestScrapperData()
        scrapper_data.class_name = 'KickerRatingsScrapper'
        scrapper_data.url_pattern = 'http\:\/\/www\.kicker\.de\/news\/fussball\/(.*)html'
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scrapped_url': my_url, 'mode': 'URL'}
        results = scrappers.FootballRatingsProcessor(
            FootballMeeting.objects.get(uuid='3173b9c6-3913-430c-837f-2cba567a9c50')).process(form, scrapper_data)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)

    def test_processor_step(self):
        my_url = 'http://fr.euro2016.infra.uefa.com/matches/libraries/2/matches'
        scrapper_data = TestFootballScrapper.TestScrapperData()
        scrapper_data.class_name = 'UEFAStepScrapper'
        #scrapper_data.url_pattern = 'http\:\/\/fr\.euro2016\.infra\.uefa\.com\/matches\/libraries\/1\/matches'
        form = TestFootballScrapper.TestForm()
        form.cleaned_data = {'scraped_url': my_url, 'mode': 'URL'}
        sfs = models.ScrappedFootballStep()
        sfs.actual_step = TournamentInstanceStep()
        results = scrappers.FootballStepProcessor(sfs).process(form, scrapper_data)
        self.assertTrue(len(results) <= 28)
        for res in results:
            print(res)