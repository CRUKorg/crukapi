from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.http import require_http_methods
from django.views.defaults import permission_denied
from jsonview.decorators import json_view


@require_http_methods(["GET"])
@json_view
def heartbeat(request):
    return {'status': 'ok'}


urlpatterns = patterns(
    '',
    # Urls for the admin site
    url(r'^djangoadmin/', include(admin.site.urls)),

    # Urls for the main portal
    url(r'^portal', include("portal.urls")),

    # Urls for the main portal
    url(r'^api', include("apis.urls")),

    # Urls for LB heath check
    url(r'^heartbeat', heartbeat, name="heartbeat"),

    url(r'', permission_denied),
)
