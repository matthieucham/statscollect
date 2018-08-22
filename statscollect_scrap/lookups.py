import datetime
from django.db.models import Case, When, Q
from selectable.base import ModelLookup

from selectable.registry import registry
from fuzzywuzzy import process

from statscollect_db.models import TournamentInstanceStep, FootballPerson, TournamentInstance, TeamMeeting

from statscollect_scrap import models


class TournamentInstanceLookup(ModelLookup):
    model = TournamentInstance
    search_fields = ('name__icontains',)

    def get_query(self, request, term):
        tournament = request.GET.get('tournament', '')
        if tournament:
            return super(TournamentInstanceLookup, self).get_query(request, term).filter(tournament=tournament)
        return list([])

    def get_item_label(self, item):
        return "%s" % item.name


class TournamentStepLookup(ModelLookup):
    model = TournamentInstanceStep
    search_fields = ('name__icontains',)

    def get_query(self, request, term):
        instance = request.GET.get('instance', '')
        if instance:
            return super(TournamentStepLookup, self).get_query(request, term).filter(tournament_instance=instance)
        return list([])

    def get_item_label(self, item):
        return "%s" % item.name


class MeetingLookup(ModelLookup):
    model = TeamMeeting

    # search_fields = ('home_team__name__icontains', 'away_team__name__icontains')

    def get_query(self, request, term):
        instance = request.GET.get('instance', '')
        step = request.GET.get('step', '')
        if step and instance:
            return super(MeetingLookup, self).get_query(request, term).filter(tournament_instance=instance,
                                                                              tournament_step=step)
        return list([])

    def get_item_label(self, item):
        return item.__str__()


class ParticipantLookup(ModelLookup):
    model = FootballPerson
    search_fields = ('last_name__icontains', 'usual_name__icontains',)


class GamesheetLookup(ModelLookup):
    model = models.ScrapedDataSheet

    def get_query(self, request, term):
        return super(GamesheetLookup, self).get_query(request, term).filter(
            source__in=['WHOSC', 'LFP']).order_by('-match_date')


class RatingsheetLookup(ModelLookup):
    model = models.ScrapedDataSheet
    search_fields = ('source__code__icontains',
                     'source__name__icontains',
                     'content__home_team__contains',
                     'content__away_team__contains',)

    def get_query(self, request, term):
        instance = request.GET.get('instance', '')
        gs = request.GET.get('gamesheet', '')
        if gs and instance:
            gamesheet = models.ScrapedDataSheet.objects.get(pk=gs)
            # Ensemble de recherche.
            sheet_choices = dict(
                [(elem['hash_url'],
                  '%s=%s' % (elem['content']['home_team'], elem['content']['away_team'])) for elem in
                 models.ScrapedDataSheet.objects.filter(Q(source__in=('HDM',)) | Q(match_date__range=(
                 datetime.datetime.combine(gamesheet.match_date.date(), datetime.time.min),
                 datetime.datetime.combine(gamesheet.match_date.date(), datetime.time.max)), )).filter(
                     Q(source__in=('FF',)) | Q(content__home_score=gamesheet.content['home_score'],
                                               content__away_score=gamesheet.content['away_score'], )).values(
                     'hash_url',
                     'content')])
            # sheet_search_key = '%s=%s' % (gamesheet.content['home_team'], gamesheet.content['away_team'])
            # print("Searching %s ..." % sheet_search_key)
            # found_ids = [sheet_id for _, _, sheet_id in
            #              process.extractBests(sheet_search_key, sheet_choices, score_cutoff=50, limit=10)]
            found_ids = sheet_choices
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(found_ids)])
            return super(RatingsheetLookup, self).get_query(request, term).filter(hash_url__in=found_ids).order_by(
                preserved)
        return list([])


registry.register(TournamentInstanceLookup)
registry.register(TournamentStepLookup)
registry.register(MeetingLookup)
registry.register(ParticipantLookup)
registry.register(GamesheetLookup)
registry.register(RatingsheetLookup)
