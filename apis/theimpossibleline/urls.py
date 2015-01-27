from django.conf.urls import patterns, url
from apis.theimpossibleline import views

urlpatterns = patterns(
    '',

    url(r'/*$',
        views.info,
        name='api_projects_impossible_line_info'),
)
