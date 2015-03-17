import re
from lxml import html
import requests
import time
import locale


class FootballGamePivot():
    """
    FootballGamePivot is a structure holding scrapped textual info about a game that is to be treated by the data
    matching processor.
    """

    def __init__(self, game_date, home_team, home_goals, away_team, away_goals):
        self.game_date = game_date
        self.home_team_name = home_team
        self.away_team_name = away_team
        self.home_team_goals = home_goals
        self.away_team_goals = away_goals


class FootballStepScrapper():
    url_pattern = r'^http'

    def scrap(self, url):
        if not re.match(self.url_pattern, url):
            raise ValueError('Input url %s does not match the expected url pattern of this scrapper. Scrapper\'s url '
                             'pattern is %s' % (url, self.url_pattern))
        page = requests.get(url)
        return self.scrap_games(page)

    def scrap_games(self, page):
        raise NotImplementedError('scrap_games must be implemented by subclasses')


class LFPFootballStepScrapper(FootballStepScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lfp\.fr\/competitionPluginCalendrierResultat' \
                           r'\/changeCalendrierHomeJournee\?c\=ligue1\&js\=[0-9]+'
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_games(self, page):
        tree = html.fromstring(page.text)
        game_days = tree.xpath('//table')

        result = []

        for gd in game_days:
            french_date = gd.xpath('preceding-sibling::h4[1]/text()')
            scrapped_games = gd.xpath('tr')
            for game in scrapped_games:
                game_hour = game.xpath('td[@class="horaire"]/a/text()')[0].strip()
                home = game.xpath('td[@class="domicile"]/a/text()')[0].strip()
                away = game.xpath('td[@class="exterieur"]/a/text()')[0].strip()
                score = game.xpath('td[@class="stats"]/a/text()')[0].strip().split(' - ')
                game_date = time.strptime(french_date[0] + ' ' + game_hour, '%A %d %B %Y %H:%M')
                score_dom = score[0]
                score_ext = score[1]
                result.append(FootballGamePivot(game_date, home, score_dom, away, score_ext))

        return result

class LEquipeFootballStepScrapper(FootballStepScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lequipe\.fr\/Football' \
                           r'\/FootballResultat[0-9]{5}\.html$'
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_games(self, page):
        tree = html.fromstring(page.text)
        games = tree.xpath('//div[@idmatch]')

        result = []

        for game in games:
            french_date = game.xpath('preceding-sibling::h2[1]/text()')
            print(french_date)
            game_hour = game.xpath('div[@class="heure "]/text()')[0].strip()
            home = game.xpath('div[@class="equipeDom"]/a/text()')[0].strip()
            away = game.xpath('div[@class="equipeExt"]/a/text()')[0].strip()
            score = game.xpath('div[@class="score"]/a/text()')[0].strip().split('-')
            game_date = time.strptime(french_date[0] + ' ' + game_hour, '%A %d %B %Y %Hh%M')
            score_dom = score[0]
            score_ext = score[1]
            result.append(FootballGamePivot(game_date, home, score_dom, away, score_ext))

        return result


