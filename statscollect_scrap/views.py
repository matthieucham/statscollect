import json
import dateutil.parser
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

from .models import ScrapedDataSheet
from .serializers import ScrapedDataSheetSerializer


class ScrapedDataSheetViewSet(viewsets.ModelViewSet):
    queryset = ScrapedDataSheet.objects.all()
    serializer_class = ScrapedDataSheetSerializer
    lookup_field = 'hash_url'
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        serializer.save()


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def scraped_datasheet_detail(request, hash_url):
    item_json = request.data
    data = dict()
    data['source'] = item_json.pop('source')
    data['content'] = item_json
    data['hash_url'] = hash_url
    data['match_date'] = dateutil.parser.parse(item_json['match_date'])

    try:
        instance = ScrapedDataSheet.objects.get(pk=hash_url)
    except ScrapedDataSheet.DoesNotExist:
        instance = None
    serializer = ScrapedDataSheetSerializer(data=data, instance=instance)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
