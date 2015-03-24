from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from portal.views import hello_world, portal_home, portal_login, api_theimpossibleline

urlpatterns = patterns(
    '',
    url(r'^hello', hello_world, name='hello_world'),

    # rules that do not require user authntication
    url(r'^login$', portal_login, name='portal_login'),
    url(r'^api/theimpossibleline', api_theimpossibleline, name="portal_api_theimpossibleline"),

    url(r'^logout', logout, {'next_page': '/'}, name='portal_logout'),

    # Rule to catch empty urls
    url(r'', portal_home, name='portal_home'),
)
