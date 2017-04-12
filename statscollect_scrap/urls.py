from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^datasheets/(?P<hash_url>[a-f0-9]{8,})/$',
        views.scraped_datasheet_detail),
]