import json

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
@permission_classes((permissions.AllowAny, ))
def scraped_datasheet_detail(request, hash_url):
    item_json = request.data
    data = dict()
    data['source'] = item_json.pop('source')
    data['content'] = item_json
    data['hash_url'] = hash_url
    serializer = ScrapedDataSheetSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def ping_view(request):
    return JsonResponse({'ping': request.data}, safe=False)