from rest_framework import viewsets

from statscollect_db.models import RatingSource
from statscollect_db.serializers import RatingSourceSerializer


class RatingSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RatingSource.objects.all()
    serializer_class = RatingSourceSerializer
    lookup_field = 'uuid'