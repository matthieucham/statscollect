import re
from lxml import html
import requests
import time
import locale
from datetime import datetime
from time import mktime
import json


class FootballGamePivot():
    """
    FootballGamePivot is a structure holding scrapped textual info about a game that is to be treated by the data
    matching processor.
    """

    def __init__(self, game_date_time, read_date, home_team, home_goals, away_team, away_goals):
        if game_date_time is not None:
            self.game_date = datetime.fromtimestamp(mktime(game_date_time))
        else:
            self.game_date = None
        self.read_date = read_date
        self.home_team_name = home_team
        self.away_team_name = away_team
        self.home_team_goals = home_goals
        self.away_team_goals = away_goals


class BaseScrapper():
    url_pattern = r'^http'

    def scrap(self, url):
        if not re.match(self.url_pattern, url):
            raise ValueError('Input url %s does not match the expected url pattern of this scrapper. Scrapper\'s url '
                             'pattern is %s' % (url, self.url_pattern))
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        page = requests.get(url, headers=headers)
        print("Page encoding= %s" % page.encoding)
        return self.scrap_page(page)

    def scrap_page(self, page):
        raise NotImplementedError('scrap_page must be implemented by subclasses')


class LFPFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lfp\.fr\/competitionPluginCalendrierResultat' \
                           r'\/changeCalendrierHomeJournee\?c\=ligue1\&js\=[0-9]+'
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
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
                rd = french_date[0] + ' ' + game_hour
                try:
                    game_date = time.strptime(rd, '%A %d %B %Y %H:%M')
                except ValueError:
                    game_date = None
                score_dom = score[0]
                score_ext = score[1]
                result.append(FootballGamePivot(game_date, rd, home, score_dom, away, score_ext))

        return result


class LEquipeFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lequipe\.fr\/Football' \
                           r'\/FootballResultat[0-9]{5}\.html$'
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        page.encoding = "UTF8"
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
            rd = french_date[0] + ' ' + game_hour
            try:
                game_date = time.strptime(rd, '%A %d %B %Y '
                                              '%Hh%M')
            except ValueError:
                game_date = None
            score_dom = score[0]
            score_ext = score[1]
            result.append(FootballGamePivot(game_date, rd, home, score_dom, away, score_ext))

        return result


class GamesheetParticipantPivot():
    def __init__(self, read_player, read_team, is_home):
        self.read_player = read_player
        self.read_team = read_team
        self.is_home = is_home


class LFPFootballGamesheetScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lfp\.fr\/ligue1\/feuille_match\/showInfosMatch\?matchId\=[0-9]{5}'
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        tree = html.fromstring(page.text)
        titulaires = tree.xpath('//h2[text()="Titulaires"]')
        result = []
        for block_titulaires in titulaires:
            homeplayers = block_titulaires.xpath('following-sibling::div[@class="domicile"][1]/ul/li/a/@href')
            awayplayers = block_titulaires.xpath('following-sibling::div[@class="exterieur"][1]/ul/li/a/@href')
            for pl in homeplayers:
                name = pl.strip()[len('/joueur/'):].replace('-', ' ')
                result.append(GamesheetParticipantPivot(name, None, True))
            for pl in awayplayers:
                name = pl.strip()[len('/joueur/'):].replace('-', ' ')
                result.append(GamesheetParticipantPivot(name, None, False))
        return result


class WhoscoredFootballGamesheetScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.whoscored\.com\/Matches\/[0-9]{6}\/Live'
        try:
            locale.setlocale(locale.LC_ALL, 'eng_gbr')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_GB')  # only on linux

    def scrap_page(self, page):
        tree = html.fromstring(page.text)
        javascript_stats = tree.xpath('//div[@id="layout-content-wrapper"]/script[@type="text/javascript"]/text('
                                      ')')
        # extract javascript array named matchCentreData
        pattern = r"(?:matchCentreData =)(.*);"
        m = re.search(pattern, javascript_stats[0]).group().strip()[len('matchCentreData ='):][:-1]
        # load string array (json notation) into python dict:
        deserz = json.loads(m)
        result = []
        for pl in deserz['home']['players']:
            if ('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl):
                result.append(GamesheetParticipantPivot(pl['name'], None, True))

        for pl in deserz['away']['players']:
            if ('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl):
                result.append(GamesheetParticipantPivot(pl['name'], None, False))
        return result