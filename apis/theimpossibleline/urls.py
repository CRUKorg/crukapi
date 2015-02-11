from django.conf.urls import patterns, url
from apis.theimpossibleline import views

urlpatterns = patterns(
    '',

    url(r'/signupmm$',
        views.proxy,
        name='api_projects_impossible_line_signup'),

    url(r'/login$',
        views.proxy,
        name='api_projects_impossible_line_login'),

    url(r'/workflows/\w+/classifications',
        views.proxy,
        name='api_projects_impossible_line_classification'),

    url(r'/subjects',
        views.proxy,
        name='api_projects_impossible_line_subjects'),

    url(r'^/*$',
        views.proxy,
        name='api_projects_impossible_line_info'),
)
