from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.defaults import permission_denied
from portal.views import hello_world

urlpatterns = patterns(
    '',
    # Urls for the admin site
    url(r'^djangoadmin/', include(admin.site.urls)),

    # Urls for the main portal functions matches anything not caught by any other handler
    url(r'^portal', include("portal.urls")),

    url(r'', permission_denied)
)
