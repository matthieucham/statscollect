from selectable.base import ModelLookup
from selectable.registry import registry

from statscollect_db.models import TournamentInstanceStep, Person, TournamentInstance, TeamMeeting


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
    model = Person
    search_fields = ('first_name__icontains', 'last_name__icontains', 'usual_name__icontains',)


registry.register(TournamentInstanceLookup)
registry.register(TournamentStepLookup)
registry.register(MeetingLookup)
registry.register(ParticipantLookup)