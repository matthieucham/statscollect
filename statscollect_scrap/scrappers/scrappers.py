import re
from lxml import html
import requests
import time
import locale
from datetime import datetime
from time import mktime
import json
from collections import defaultdict


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
        self.gamesheet_identifier = None


class BaseScrapper():
    url_pattern = r'^http'

    def scrap(self, url):
        m = re.match(self.url_pattern, url)
        if not m:
            raise ValueError('Input url %s does not match the expected url pattern of this scrapper. Scrapper\'s url '
                             'pattern is %s' % (url, self.url_pattern))
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        self.page_identifier = m.group(1)
        page = requests.get(url, headers=self.headers)
        print("Page encoding= %s" % page.encoding)
        return self.scrap_page(page)

    def scrap_page(self, page):
        raise NotImplementedError('scrap_page must be implemented by subclasses')


class LFPFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lfp\.fr\/competitionPluginCalendrierResultat' \
                           r'\/changeCalendrierHomeJournee\?c\=ligue1\&js\=([0-9]{1-2})+'
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
                match_id = game.xpath('td[@class="stats"]/a/@href')[0].strip()[len('/ligue1/feuille_match/'):]
                rd = french_date[0] + ' ' + game_hour
                try:
                    game_date = time.strptime(rd, '%A %d %B %Y %H:%M')
                except ValueError:
                    game_date = None
                score_dom = score[0]
                score_ext = score[1]
                pivot = FootballGamePivot(game_date, rd, home, score_dom, away, score_ext)
                pivot.gamesheet_identifier = match_id
                result.append(pivot)

        return result


class LEquipeFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lequipe\.fr\/Football' \
                           r'\/FootballResultat([0-9]{5})\.html$'
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
    def __init__(self, read_player, read_team, is_home=None):
        self.read_player = read_player
        self.read_team = read_team
        self.is_home = is_home
        if (not read_team) and (is_home is not None):
            if is_home:
                self.read_team = 'HOME'
            else:
                self.read_team = 'AWAY'


class LFPFootballGamesheetScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.lfp\.fr\/ligue1\/feuille_match\/showInfosMatch\?matchId\=([0-9]{5})'
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


class WhoscoredMatchDataExtractor:
    def extract(self, page_text):
        tree = html.fromstring(page_text)
        javascript_stats = tree.xpath('//div[@id="layout-content-wrapper"]/script[@type="text/javascript"]/text('
                                      ')')
        # extract javascript array named matchCentreData
        pattern = r"(?:matchCentreData =)(.*);"
        m = re.search(pattern, javascript_stats[0]).group().strip()[len('matchCentreData ='):][:-1]
        # load string array (json notation) into python dict:
        return json.loads(m)


class WhoscoredFGSScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.whoscored\.com\/Matches\/([0-9]{6})\/Live'
        try:
            locale.setlocale(locale.LC_ALL, 'eng_gbr')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_GB')  # only on linux

    def scrap_page(self, page):
        deserz = WhoscoredMatchDataExtractor().extract(page.text)
        result = []
        for pl in deserz['home']['players']:
            if ('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl):
                result.append(GamesheetParticipantPivot(pl['name'], None, True))

        for pl in deserz['away']['players']:
            if ('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl):
                result.append(GamesheetParticipantPivot(pl['name'], None, False))
        return result


class WhoscoredStatsScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = r'^http\:\/\/www\.whoscored\.com\/Matches\/([0-9]{6})\/Live'
        try:
            locale.setlocale(locale.LC_ALL, 'eng_gbr')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_GB')  # only on linux

    def increment_or_set_key(self, target_dict, key):
        if not key in target_dict:
            target_dict[key] = 1
        else:
            target_dict[key] += 1

    def scrap_page(self, page):
        deserz = WhoscoredMatchDataExtractor().extract(page.text)
        result = []

        total_time = deserz['maxMinute'] + 1
        out_time = {}
        in_time = {}
        goals_time = {'home': [], 'away': []}

        event_stats = {}
        # incremental stats
        for field in ['home', 'away']:
            for ev in deserz[field]['incidentEvents']:
                if 'playerId' in ev:
                    if not ev['playerId'] in event_stats:
                        event_stats[ev['playerId']] = {}
                if 'cardType' in ev:
                    if ev['cardType']['displayName'] in ['SecondYellow', 'Red']:
                        out_time[ev['playerId']] = ev['minute']
                elif 'SubstitutionOff' == ev['type']['displayName']:
                    out_time[ev['playerId']] = ev['minute']
                elif 'SubstitutionOn' == ev['type']['displayName']:
                    in_time[ev['playerId']] = ev['minute']
                elif 'Goal' == ev['type']['displayName']:
                    if 'isOwnGoal' in ev:
                        goals_time['away' if field == 'home' else 'home'].append(ev['minute'])
                        self.increment_or_set_key(event_stats[ev['playerId']], 'og')
                    else:
                        goals_time[field].append(ev['minute'])
                        is_penalty = False
                        for q in ev['qualifiers']:
                            if 'Penalty' == q['type']['displayName']:
                                is_penalty = True
                                break
                        if is_penalty:
                            self.increment_or_set_key(event_stats[ev['playerId']], 'penalties')
                        else:
                            self.increment_or_set_key(event_stats[ev['playerId']], 'goals')
                elif 'Pass' == ev['type']['displayName']:
                    for q in ev['qualifiers']:
                        if 'IntentionalGoalAssist' == q['type']['displayName']:
                            self.increment_or_set_key(event_stats[ev['playerId']], 'assists')
                            break
        # global stats (the first loop must have been completed
        read_stats = {}
        ordered_plid = []
        for field in ['home', 'away']:
            conceded_goals = goals_time['away' if field == 'home' else 'home']
            conceded_goals.sort()
            for pl in deserz[field]['players']:
                if not (('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl)):
                    continue
                read_stats[pl['playerId']] = {}
                ordered_plid.append(pl['playerId'])
                if pl['playerId'] in event_stats:
                    read_stats[pl['playerId']] = event_stats[pl['playerId']]
                read_stats[pl['playerId']]['team'] = field
                read_stats[pl['playerId']]['saves'] = len(pl['stats']['totalSaves']) if 'totalSaves' in pl['stats'] \
                    else 0
                if 'isFirstEleven' in pl:
                    if pl['playerId'] in out_time:
                        read_stats[pl['playerId']]['playtime'] = out_time[pl['playerId']]
                        read_stats[pl['playerId']]['conceded'] = len(
                            list(filter((lambda x: x <= out_time[pl['playerId']]), conceded_goals)))
                    else:
                        read_stats[pl['playerId']]['playtime'] = total_time
                        read_stats[pl['playerId']]['conceded'] = len(conceded_goals)
                elif pl['position'] == 'Sub' and 'subbedInExpandedMinute' in pl:
                    if pl['playerId'] in out_time:
                        read_stats[pl['playerId']]['playtime'] = out_time[pl['playerId']] - in_time[pl['playerId']]
                        read_stats[pl['playerId']]['conceded'] = len(list(filter((lambda x: x <= out_time[pl[
                            'playerId']]
                                                                                            and x >= in_time[
                            pl['playerId']]
                                                                                 ), conceded_goals)))
                    else:
                        read_stats[pl['playerId']]['playtime'] = total_time - in_time[pl['playerId']]
                        read_stats[pl['playerId']]['conceded'] = len(list(filter((lambda x: x >= in_time[pl[
                            'playerId']]),
                                                                                 conceded_goals)))
        # convert read_stats to players_stat_list
        for plid in ordered_plid:
            pl_name = deserz['playerIdNameDictionary'][str(plid)]
            read_stats[plid]['read_player'] = pl_name
            result.append(read_stats[plid])
        return result