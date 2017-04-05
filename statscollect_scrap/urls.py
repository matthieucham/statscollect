from django.conf.urls import url

from .views import ScrapedDataSheetViewSet


urlpatterns = [
    url(r'^datasheets/$', ScrapedDataSheetViewSet.as_view({'get': 'list', }, suffix='List'), name='datasheet-list'),
    url(r'^datasheets/(?P<hash_url>[a-f0-9]{8,})/$',
        ScrapedDataSheetViewSet.as_view({'get': 'retrieve', 'post': 'create', }), name='datasheet-detail'),
]