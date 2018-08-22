__author__ = 'Matt'
import dateutil.parser
import logging
from fuzzywuzzy import process, fuzz
from unidecode import unidecode

from statscollect_scrap import models
from statscollect_scrap.scrappers import myfuzz
from statscollect_db.models import FootballTeam, FootballPerson, AlternativePersonName


class GamesheetProcessor():
    logger = logging.getLogger('django')

    # Ensemble de recherche.
    team_choices_preferred = dict(
        [(elem['id'], unidecode(elem['name'])) for elem in FootballTeam.objects.all().values('id', 'name')])
    team_choices_secondary = dict(
        [(elem['id'], unidecode(elem['short_name'])) for elem in FootballTeam.objects.all().values('id',
                                                                                                   'short_name')])

    def process(self, processedgame):
        summary = self._process_summary(processedgame.gamesheet_ds.content)
        if not (summary.home_team and summary.away_team):
            raise ValueError("Could not scrap GameSummary: teams not matched")
        # delete previous if any:
        models.ProcessedGameSummary.objects.filter(processed_game=processedgame).delete()
        # set the new one
        summary.processed_game = processedgame
        summary.save()

        hchoices, achoices = self._get_choices(summary.home_team, summary.away_team)
        haltchoices, aaltchoices = self._get_alternative_choices(summary.home_team, summary.away_team)

        players = self._process_players(processedgame.gamesheet_ds.content,
                                        {'home': hchoices, 'away': achoices},
                                        {'home': haltchoices, 'away': aaltchoices},
                                        {'home': summary.home_team, 'away': summary.away_team})
        # delete previous if any:
        models.ProcessedGameSheetPlayer.objects.filter(processed_game=processedgame).delete()
        # register scraped players
        for pl in players:
            pl.processed_game = processedgame
            pl.save()
        for ds in processedgame.rating_ds.all():
            ratings = self._process_ratings(ds.source, ds.content,
                                            {'home': hchoices, 'away': achoices},
                                            {'home': haltchoices, 'away': aaltchoices})
            # delete previous if any:
            models.ProcessedGameRating.objects.filter(processed_game=processedgame, rating_source=ds.source).delete()
            # register scraped players
            for pl in ratings:
                pl.processed_game = processedgame
                pl.save()
        processedgame.status = 'PENDING'
        processedgame.save()

    def _get_choices(self, home_team, away_team):
        return dict(
            [(elem['id'], unidecode(
                elem['first_name'][:3] + ' ' + elem['last_name'] + ' ' + elem['usual_name']))
             for elem in
             FootballPerson.objects.filter(current_teams=home_team).values('id', 'first_name', 'last_name',
                                                                           'usual_name')]
        ), dict(
            [(elem['id'], unidecode(elem['first_name'][:3] + ' ' + elem['last_name'] + ' ' + elem['usual_name']))
             for elem in
             FootballPerson.objects.filter(current_teams=away_team).values('id', 'first_name', 'last_name',
                                                                           'usual_name')]
        )

    def _get_alternative_choices(self, home_team, away_team):
        return dict(
            [(elem['person_id'], unidecode(elem['alt_name']))
             for elem in
             AlternativePersonName.objects.filter(person__current_teams=home_team).values('person_id', 'alt_name')]
        ), dict(
            [(elem['person_id'], unidecode(elem['alt_name']))
             for elem in
             AlternativePersonName.objects.filter(person__current_teams=away_team).values('person_id', 'alt_name')]
        )

    def _process_ratings(self, src, data, choices, alternative):
        for key in ['home', 'away']:
            for pl in data['players_' + key]:
                teammeetingperson, ratio = self._find_person(pl['name'], choices[key], alternative[key])
                try:
                    rt = float(pl['rating']) if pl['rating'] else None
                except ValueError:
                    rt = None
                yield models.ProcessedGameRating(scraped_name=pl['name'], scraped_ratio=ratio,
                                                 footballperson=teammeetingperson,
                                                 rating=rt,
                                                 rating_source=src)

    def _process_players(self, data, choices, altchoices, teams):
        for key in ['home', 'away']:
            for pl in data['players_' + key]:
                teammeetingperson, ratio = self._find_person(pl['name'], choices[key], altchoices[key])
                stats = pl.get('stats', {})
                yield models.ProcessedGameSheetPlayer(scraped_name=pl['name'], scraped_ratio=ratio,
                                                      footballperson=teammeetingperson,
                                                      team=teams[key],
                                                      playtime=int(stats.get('playtime', 0)),
                                                      goals_scored=int(stats.get('goals_scored', 0)),
                                                      penalties_scored=int(stats.get('penalties_scored', 0)),
                                                      goals_assists=int(stats.get('goals_assists', 0)),
                                                      penalties_assists=int(stats.get('penalties_assists', 0)),
                                                      goals_saves=int(stats.get('goals_saved', 0)),
                                                      goals_conceded=int(stats.get('goals_conceded', 0)),
                                                      own_goals=int(stats.get('own_goals', 0)),
                                                      )

    def _process_summary(self, data):
        home_team, away_team = self._find_teams(data)
        home_score, away_score = int(data['home_score']), int(data['away_score'])
        match_date = dateutil.parser.parse(data['match_date'])
        return models.ProcessedGameSummary(home_team=home_team, away_team=away_team, home_score=home_score,
                                           away_score=away_score, game_date=match_date)

    def _find_person(self, player_name, choices, alternative_choices):
        self.logger.info('Searching %s' % player_name)
        matching_results = process.extractBests(unidecode(player_name), choices,
                                                scorer=fuzz.partial_token_set_ratio,
                                                score_cutoff=75)
        try:
            return self._refine_matching_results(player_name, matching_results)
        except AssertionError:
            self.logger.warning("Alert : no match for %s" % player_name)
            self.logger.info("Now searching with alternative names for %s" % player_name)
            matching_results = process.extractBests(unidecode(player_name), alternative_choices,
                                                    scorer=fuzz.partial_token_set_ratio,
                                                    score_cutoff=90)
            try:
                return self._refine_matching_results(player_name, matching_results)
            except AssertionError:
                self.logger.warning("Alert : no match AT ALL for %s" % player_name)
            return None, 0.0

    def _refine_matching_results(self, player_name, matching_results):
        assert len(matching_results) > 0
        # si les meilleurs matchs sont à egalité de score, chercher à nouveau avec méthode différente
        best_score = 0
        creme = dict()
        for name, score, plid in matching_results:
            if score >= best_score:
                best_score = score
                creme.update({plid: name})
            else:
                # la liste renvoyée par extractBests est triée donc on peut s'arreter dès que le niveau baisse.
                break
        # combien de meilleurs scores ?
        if len(creme) == 1:
            plid, plname = creme.popitem()
            self.logger.info('Found %s at first round with ratio %s' % (plname, best_score))
            matching_player = FootballPerson.objects.get(pk=plid)
            return matching_player, best_score
        else:
            self.logger.info('Multiple matches found with ratio %s, refining...' % best_score)
            refine_results = process.extractBests(unidecode(player_name), creme,
                                                  scorer=myfuzz.partial_token_set_ratio_with_avg)
            plname, ratio, plid = refine_results[0]
            self.logger.info('Found %s at second round with ratio %s then %s' % (plname, best_score, ratio))
            matching_player = FootballPerson.objects.get(pk=plid)
            return matching_player, best_score

    def _find_teams(self, datasheet):
        ht = self._search_team(datasheet['home_team'])
        at = self._search_team(datasheet['away_team'])
        return ht, at

    def _search_team(self, team_name):
        self.logger.info('Searching %s' % team_name)
        matching_results = process.extractBests(unidecode(team_name), self.team_choices_preferred,
                                                score_cutoff=80,
                                                limit=1)
        if len(matching_results) == 0:
            self.logger.warning('No result in long names. Searching %s in short names...' % team_name)
            # search again with secondary choices this time.
            matching_results = process.extractBests(team_name,
                                                    self.team_choices_secondary,
                                                    score_cutoff=50,
                                                    limit=1)
        if len(matching_results) > 0:
            home_result, ratio, team_id = matching_results[0]
            self.logger.info('Found %s with ratio %d' % (home_result, ratio))
            matching_team = FootballTeam.objects.get(pk=team_id)
            return matching_team
            self.logger.warning("Alert : no valid match for %s" % team_name)
        return None
