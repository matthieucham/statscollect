from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^ping/$', views.ping_view),
    url(r'^datasheets/$', views.scraped_datasheet_detail),
    url(r'^datasheets/(?P<hash_url>[a-f0-9]{8,})/$',
        views.ScrapedDataSheetViewSet.as_view({'get': 'retrieve', }), name='datasheet-detail'),
]