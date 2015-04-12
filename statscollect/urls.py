from django.conf.urls import patterns, include, url

from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'statscollect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^rest/', include('statscollect_db.urls')),
    url(r'^scrap/', include('statscollect_scrap.urls', namespace='scrap')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^selectable/', include('selectable.urls')),
)
