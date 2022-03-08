from django.conf.urls import include, url
from django.contrib import admin

from statscollect_db.frontend import HomePage

urlpatterns = [
    url(r"^$", HomePage.as_view(), name="homepage"),
    url(r"^rest/", include("statscollect_db.urls")),
    url(
        r"^scrap/",
        include("statscollect_scrap.urls"),
        name="scrap",
    ),
    url(r"^admin/", admin.site.urls),
    url(
        r"^api-auth/",
        include("rest_framework.urls"),
        name="rest_framework",
    ),
    url(r"^o/", include("oauth2_provider.urls"), name="oauth2_provider"),
    url(r"^chaining/", include("smart_selects.urls")),
]
