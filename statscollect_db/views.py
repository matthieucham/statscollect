from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.parsers import JSONParser
from statscollect_db.models import RatingSource
from statscollect_db.serializers import RatingSourceSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


@api_view(['GET', 'POST'])
def rating_source_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        rating_sources = RatingSource.objects.all()
        serializer = RatingSourceSerializer(rating_sources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RatingSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def rating_source_detail(request, uuid, format=None):
    """
    Retrieve, update or delete a rating source.
    """
    try:
        snippet = RatingSource.objects.get(uuid=uuid)
    except RatingSource.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSourceSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RatingSourceSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)