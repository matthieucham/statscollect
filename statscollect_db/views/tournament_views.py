from rest_framework import viewsets

from statscollect_db.models import Tournament, TournamentInstance
from statscollect_db.serializers import TournamentSerializer, TournamentInstanceSerializer


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = 'uuid'
    filter_fields = (
        'uuid',
        'field',
        'type',
    )


class TournamentInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentInstanceSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        tournament = self.kwargs.get('tournament')
        if tournament is not None:
            queryset = TournamentInstance.objects.filter(
                tournament__uuid__contains=tournament
            )
            return queryset
        return TournamentInstance.objects.all()

