from rest_framework import viewsets

from .models import ScrapedDataSheet
from .serializers import ScrapedDataSheetSerializer


class ScrapedDataSheetViewSet(viewsets.ModelViewSet):
    queryset = ScrapedDataSheet.objects.all()
    serializer_class = ScrapedDataSheetSerializer
    lookup_field = 'hash_url'