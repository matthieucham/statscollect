from selectable.base import ModelLookup
from selectable.registry import registry

from statscollect_db.models import TournamentInstanceStep, FootballPerson, TournamentInstance, TeamMeeting, RatingSource
from statscollect_scrap import models


class TournamentInstanceLookup(ModelLookup):
    model = TournamentInstance
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        tournament = request.GET.get('tournament', '')
        if tournament:
            return super(TournamentInstanceLookup, self).get_query(request, term).filter(tournament=tournament)
        return list([])

    def get_item_label(self, item):
        return "%s" % item.name


class TournamentStepLookup(ModelLookup):
    model = TournamentInstanceStep
    search_fields = ('name__icontains', )

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
                     'source__name__icontains', 'content__home_team__contains', 'content__away_team__contains',)

    def get_query(self, request, term):
        instance = request.GET.get('instance', '')
        gs = request.GET.get('gamesheet', '')
        if gs and instance:
            gamesheet = models.ScrapedDataSheet.objects.get(pk=gs)
            return super(RatingsheetLookup, self).get_query(request, term).filter(
                source__expected_set__tournament_instance=instance, match_date__year=gamesheet.match_date.year,
                match_date__month=gamesheet.match_date.month, match_date__day=gamesheet.match_date.day)
        return list([])


registry.register(TournamentInstanceLookup)
registry.register(TournamentStepLookup)
registry.register(MeetingLookup)
registry.register(ParticipantLookup)
registry.register(GamesheetLookup)
registry.register(RatingsheetLookup)