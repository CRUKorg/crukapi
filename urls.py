from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.defaults import permission_denied

urlpatterns = patterns(
    '',
    # Urls for the admin site
    url(r'^djangoadmin/', include(admin.site.urls)),

    # Urls for the main portal
    url(r'^portal', include("portal.urls")),

    # Urls for the main portal
    url(r'^api', include("apis.urls")),

    url(r'', permission_denied)
)
