import re
import os
from lxml import html
import time
import locale
from datetime import datetime
from time import mktime
import json


class BaseScrapper():
    def scrap_page(self, page):
        raise NotImplementedError('scrap_page must be implemented by subclasses')


class FakeScrapper():
    def scrap_page(self, page):
        pass


class LFPFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = "http\:\/\/www\.lfp\.fr\/competitionPluginCalendrierResultat\/changeCalendrierHomeJournee" \
                           "\?c\=ligue1\&js\=([0-9]{1,2})+"
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        tree = html.fromstring(page)
        game_days = tree.xpath('//table')

        result = []

        for gd in game_days:
            french_date = gd.xpath('preceding-sibling::h4[1]/text()')
            scrapped_games = gd.xpath('tr')
            for game in scrapped_games:
                try:
                    sg = {}
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
                    output = {'read_game_date': rd, 'read_home_team': home,
                              'read_away_team': away, 'home_score': score_dom, 'away_score': score_ext}
                    if game_date:
                        output['actual_game_date'] = datetime.fromtimestamp(mktime(game_date))

                    result.append(output)
                except IndexError:
                    pass
        return result


class LEquipeFootballStepScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = "http\:\/\/www\.lequipe\.fr\/Football\/FootballResultat([0-9]{5})\.html$"
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        tree = html.fromstring(page)
        games = tree.xpath('//div[@idmatch]')

        result = []

        for game in games:
            try:
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
                output = {'read_game_date': rd, 'read_home_team': home,
                          'read_away_team': away, 'home_score': score_dom, 'away_score': score_ext}
                if game_date:
                    output['actual_game_date'] = datetime.fromtimestamp(mktime(game_date))

                result.append(output)
            except IndexError:
                pass
        return result


class LFPFootballGamesheetScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = "http\:\/\/www\.lfp\.fr\/ligue1\/feuille_match\/showInfosMatch\?matchId\=([0-9]{5})"
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        tree = html.fromstring(page)
        titulaires = tree.xpath('//h2[text()="Titulaires"]')
        result = []
        for block_titulaires in titulaires:
            homeplayers = block_titulaires.xpath('following-sibling::div[@class="domicile"][1]/ul/li/a/@href')
            awayplayers = block_titulaires.xpath('following-sibling::div[@class="exterieur"][1]/ul/li/a/@href')
            for pl in homeplayers:
                name = pl.strip()[len('/joueur/'):].replace('-', ' ')
                result.append({'read_player': name, 'read_team': 'domicile', 'is_home': True})
            for pl in awayplayers:
                name = pl.strip()[len('/joueur/'):].replace('-', ' ')
                result.append({'read_player': name, 'read_team': 'exterieur', 'is_home': False})
        return result


def extract_ws_matchdata(page_text):
    tree = html.fromstring(page_text)
    javascript_stats = tree.xpath('//div[@id="layout-content-wrapper"]/script[@type="text/javascript"]/text('
                                  ')')
    # javascript_stats = robobrowser.find(id="layout-content-wrapper").find("script", type="text/javascript").string
    # extract javascript array named matchCentreData
    pattern = r"(?:matchCentreData =)(.*);"
    m = re.search(pattern, javascript_stats[0]).group().strip()[len('matchCentreData ='):][:-1]
    # load string array (json notation) into python dict:
    return json.loads(m)


class WhoscoredFGSScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = "http\:\/\/www\.whoscored\.com\/Matches\/([0-9]{6,7})\/Live"
        try:
            locale.setlocale(locale.LC_ALL, 'eng_gbr')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'en_GB')  # only on linux

    def scrap_page(self, page):
        deserz = extract_ws_matchdata(page)
        result = []
        for field in ['home', 'away']:
            for pl in deserz[field]['players']:
                if ('isFirstEleven' in pl) or ('subbedInExpandedMinute' in pl):
                    result.append({'read_player': pl['name'], 'read_team': field, 'is_home': field == 'home'})
        return result


class WhoscoredStatsScrapper(BaseScrapper):
    def __init__(self):
        self.url_pattern = "http\:\/\/www\.whoscored\.com\/Matches\/([0-9]{6,7})\/Live"
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
        deserz = extract_ws_matchdata(page)
        result = []

        total_time = deserz['maxMinute'] + 1
        out_time = {}
        in_time = {}
        goals_time = {'home': [], 'away': []}

        event_stats = {}

        # incremental stats
        for field in ['home', 'away']:
            goal_related_events = []
            for ev in deserz[field]['incidentEvents']:
                if 'playerId' in ev:
                    if not ev['playerId'] in event_stats:
                        event_stats[ev['playerId']] = {}
                try:
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
                            self.increment_or_set_key(event_stats[ev['playerId']], 'own_goals')
                        else:
                            goals_time[field].append(ev['minute'])
                            is_penalty = False
                            for q in ev['qualifiers']:
                                if 'Penalty' == q['type']['displayName']:
                                    is_penalty = True
                                    break
                            if is_penalty:
                                self.increment_or_set_key(event_stats[ev['playerId']], 'penalties_scored')
                            else:
                                for q in ev['qualifiers']:
                                    if 'RelatedEventId' == q['type']['displayName']:
                                        goal_related_events.append(q['value'])
                                        break
                                self.increment_or_set_key(event_stats[ev['playerId']], 'goals_scored')
                except KeyError:
                    pass
            # Loop again to find passes
            for ev in deserz[field]['incidentEvents']:
                if 'Pass' == ev['type']['displayName']:
                    self.increment_or_set_key(event_stats[ev['playerId']], 'assists')
                elif str(ev['eventId']) in goal_related_events:
                    for q in ev['qualifiers']:
                        if q['type']['displayName'] in ('IntentionalGoalAssist', 'IntentionalAssist', 'KeyPass',):
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
                        read_stats[pl['playerId']]['conceded'] = len(
                            list(
                                filter(
                                    (lambda x: x <= out_time[pl['playerId']] and x >= in_time[pl['playerId']]),
                                    conceded_goals
                                )
                            )
                        )
                    else:
                        read_stats[pl['playerId']]['playtime'] = total_time - in_time[pl['playerId']]
                        read_stats[pl['playerId']]['conceded'] = len(
                            list(
                                filter(
                                    (lambda x: x >= in_time[pl['playerId']]),
                                    conceded_goals
                                )
                            )
                        )
        # convert read_stats to players_stat_list
        for plid in ordered_plid:
            pl_name = deserz['playerIdNameDictionary'][str(plid)]
            read_stats[plid]['read_player'] = pl_name
            result.append(read_stats[plid])
        return result


class OrangeRatingsScrapper(BaseScrapper):
    url_pattern = "http\:\/\/sports\.orange\.fr\/football\/ligue\-1\/match\/(.*).html"

    def scrap_page(self, page):
        print('Scrappingwith OrangeRatingsScrapper')
        tree = html.fromstring(page)
        strong_in_article = tree.xpath('//div[@itemprop="articleBody"]/p//strong')
        result = []
        # homep = article[0].xpath('p[last()-1]/strong')
        # awayp = article[0].xpath('p[last()]/strong')
        name_pattern = r'(?:puis )*([\w][\w|àéèäëâêiîïöôûüù\- ]+)[\s]*(?:\(cap\))*[\s]*\((?:[\d]+[^,\-]+(?:\-[\s])*)*$'
        next_is_home = False
        next_is_away = False
        home_pars = []
        homep_to_search = None
        away_pars = []
        awayp_to_search = None
        for par in strong_in_article:
            if par.text is not None and par.text.startswith('Expulsion'):
                next_is_home = True
            elif next_is_home:
                home_pars.append(par.xpath('following-sibling::br[1]')[0])
                homep_to_search = par.xpath('following-sibling::strong')
                next_is_home = False
            elif par.text is not None and par.text.startswith('Entraîneur') and awayp_to_search is None:
                next_is_away = True
            elif next_is_away:
                away_pars.append(par.xpath('following-sibling::br[1]')[0])
                awayp_to_search = par.xpath('following-sibling::strong')
                next_is_away = False
        if homep_to_search is None or awayp_to_search is None:
            return result
        # select relevant pars in home
        for par in homep_to_search:
            if par.text.startswith('N\'ont pas participé'):
                break
            else:
                home_pars.append(par)

        # select relevant pars in away
        for par in awayp_to_search:
            if par.text.startswith('N\'ont pas participé'):
                break
            else:
                away_pars.append(par)

        previous_tail = None
        ignore_next = False
        for blabla in home_pars:
            plrating = {'team': 'home'}
            content = blabla.text
            if content is not None:
                if content.startswith('Arbitre'):
                    ignore_next = True
                if len(content) == 1 and content.isdigit:
                    matched = re.search(name_pattern, previous_tail)
                    if matched is not None:
                        if ignore_next:
                            ignore_next = False
                        else:
                            plrating['read_player'] = matched.group(1).strip()
                            plrating['rating'] = content
                            print('Read player %s ; %s' % (plrating['read_player'], plrating['rating']))
                            result.append(plrating)
            previous_tail = blabla.tail
        previous_tail = None
        for blabla in away_pars:
            plrating = {'team': 'away'}
            content = blabla.text
            if content is not None:
                if content.startswith('Arbitre'):
                    ignore_next = True
                if len(content) == 1 and content.isdigit:
                    matched = re.search(name_pattern, previous_tail)
                    if matched is not None:
                        if ignore_next:
                            ignore_next = False
                        else:
                            plrating['read_player'] = matched.group(1).strip()
                            plrating['rating'] = content
                            print('Read player %s ; %s' % (plrating['read_player'], plrating['rating']))
                            result.append(plrating)
            previous_tail = blabla.tail
        return result


class WhoscoredRatingsScrapper(BaseScrapper):
    url_pattern = "http\:\/\/www\.whoscored\.com\/Matches\/([0-9]{6,7})\/Live"

    def scrap_page(self, page):
        deserz = extract_ws_matchdata(page)
        result = []
        for field in ['home', 'away']:
            for pl in deserz[field]['players']:
                if 'ratings' in pl['stats']:
                    max_key = max(pl['stats']['ratings'], key=int)
                    # +001 because WS rounds ...5 UP while python rounds it down.
                    mark = round(pl['stats']['ratings'][max_key] + .001, 1)
                    result.append({'read_player': pl['name'], 'rating': mark, 'team': field})
        return result


class SportsFrRatingsScrapper(BaseScrapper):
    url_pattern = "http\:\/\/www\.sports\.fr\/football\/compte\-rendu\/ligue\-1\/(.*).html"

    def scrap_page(self, page):
        tree = html.fromstring(page)
        field = tree.xpath('//div[@class="stade"]')
        result = []
        homeplayers = field[0].xpath('div[@class="compo team1"]/ul/li')
        awayplayers = field[0].xpath('div[@class="compo team2"]/ul/li')
        href_pattern = "/football/joueurs/[0-9]{1,2}/([a-z\-]+)\-[0-9]{3,6}.html"
        for pl in homeplayers:
            plrating = {'team': 'home'}
            href = pl.xpath('a/@href')[0].strip()
            plrating['read_player'] = re.match(href_pattern, href).group(1).replace('-', ' ')
            for mark in pl.xpath('a/span[@class="numero"]/text()'):
                if mark != '-':
                    plrating['rating'] = mark
            result.append(plrating)
        for pl in awayplayers:
            plrating = {'team': 'away'}
            href = pl.xpath('a/@href')[0].strip()
            plrating['read_player'] = re.match(href_pattern, href).group(1).replace('-', ' ')
            for mark in pl.xpath('a/span[@class="numero"]/text()'):
                if mark != '-':
                    plrating['rating'] = mark
            result.append(plrating)
        return result


class KickerRatingsScrapper(BaseScrapper):
    url_pattern = "http\:\/\/www\.kicker\.de\/news\/fussball\/(.*)html"

    def scrap_page(self, page):
        # dump_file = open('kicker.html', 'w')
        # dump_file.write(page)
        # dump_file.close()
        # print("Dump file at %s", os.path.abspath('kicker.html'))
        tree = html.fromstring(page)
        aufstellungen = tree.xpath('//table[@summary="Vereinsliste"]')
        result = []
        homeplayers = aufstellungen[0].xpath('//tr[@id="ctl00_PlaceHolderHalf_ctl00_heim2"]//div[@class="spielerdiv"]')
        awayplayers = aufstellungen[0].xpath('//tr[@id="ctl00_PlaceHolderHalf_ctl00_auswaerts2"]//div['
                                             '@class="spielerdiv"]')
        href_pattern = ".*/spieler_(.+).html$"
        mark_pattern = "^\(([0-9,]{1,3})\).*$"
        for pl in homeplayers:
            plrating = {'team': 'home'}
            href = pl.xpath('a/@href')[0].strip()
            m = pl.xpath('text()')[0].strip()
            plrating['read_player'] = re.match(href_pattern, href).group(1).replace('-', ' ')
            mark = re.match(mark_pattern, m)
            if mark is not None:
                plrating['rating'] = mark.group(1).replace(',', '.')
            result.append(plrating)
        for pl in awayplayers:
            plrating = {'team': 'away'}
            href = pl.xpath('a/@href')[0].strip()
            m = pl.xpath('text()')[0].strip()
            plrating['read_player'] = re.match(href_pattern, href).group(1).replace('-', ' ')
            mark = re.match(mark_pattern, m)
            if mark is not None:
                plrating['rating'] = mark.group(1).replace(',', '.')
            result.append(plrating)
        return result


class UEFAStepScrapper(BaseScrapper):
    url_pattern = "http\:\/\/fr\.euro2016\.infra\.uefa\.com\/matches\/libraries\/(.*)\/matches"

    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, 'fra_fra')  # only on windows
        except locale.Error:
            locale.setlocale(locale.LC_ALL, 'fr_FR')  # only on linux

    def scrap_page(self, page):
        # dump_file = open('uefa.html', 'w')
        # dump_file.write(page.encode('utf-8'))
        # dump_file.close()
        # print("Dump file at %s", os.path.abspath('uefa.html'))
        tree = html.fromstring(page)
        games = tree.xpath('//a[@class="match-row_link"]')

        result = []

        for gd in games:
            home = str(gd.xpath('div//span[@class="team-name_name"]/text()')[0])
            away = str(gd.xpath('div//span[@class="team-name_name"]/text()')[1])
            score = gd.xpath('div//span[@class="match--score_score"]/span/text()')
            french_date = gd.xpath('parent::div/preceding-sibling::h3/text()')[-1].strip()
            gd = time.strptime(french_date, '%A, %d %B %Y')
            output = {'read_game_date': french_date, 'read_home_team': home, 'read_away_team': away, 'home_score':
                score[0], 'away_score': score[1]}
            output['actual_game_date'] = datetime.fromtimestamp(mktime(gd))
            result.append(output)
        return result
