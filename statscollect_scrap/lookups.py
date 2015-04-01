from selectable.base import LookupBase, ModelLookup
from selectable.registry import registry

from statscollect_db.models import TournamentInstanceStep, Person


class TournamentStepLookup(ModelLookup):
    model = TournamentInstanceStep
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(TournamentStepLookup, self).get_query(request, term)
        instance = request.GET.get('instance', '')
        if instance:
            results = results.filter(tournament_instance=instance)
        return results

    def get_item_label(self, item):
        return "%s [%s]" % (item.name, item.tournament_instance.name)


class ParticipantLookup(ModelLookup):
    model = Person
    search_fields = ('first_name__icontains', 'last_name__icontains', 'usual_name__icontains',)

registry.register(TournamentStepLookup)
registry.register(ParticipantLookup)