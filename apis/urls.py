from django.conf.urls import patterns, include, url
from django.views.defaults import permission_denied

urlpatterns = patterns(
    '',

    # Project - the impossible line
    url(r'projects/impossible_line', include('apis.theimpossibleline.urls')),

    url(r'', permission_denied)
)



