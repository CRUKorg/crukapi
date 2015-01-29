from django.conf.urls import patterns, url
from apis.theimpossibleline import views

urlpatterns = patterns(
    '',

    url(r'/subjects',
        views.proxy,
        name='api_projects_impossible_line_subjects'),

    url(r'^/*$',
        views.proxy,
        name='api_projects_impossible_line_info'),
)
