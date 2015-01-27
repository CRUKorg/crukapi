import json
import sys
import urllib2
from django.conf import settings
from django.http import HttpResponse


class EngineFactory(object):

    @classmethod
    def get_engine(cls, request):
        module = sys.modules[__name__]
        engine_class = getattr(module, settings.API_IMPOSSIBLE_LINE_ENGINE)
        return engine_class(request)


class MockEngine(object):

    mock_info_json = {
        "id": "53c3e9090ab4c05d28000001",
        "activated_subjects_at": "2015-01-27T09:00:14Z",
        "classification_count": 751,
        "created_at": "2014-07-14T15:16:52Z",
        "display_name": "The Impossible Line",
        "name": "impossible_line",
        "site_prefix": "IL",
        "updated_at": "2014-07-14T15:16:52Z",
        "workflow_name": "impossible_line"}

    def __init__(self, request):
        self.request = request

    def info(self):
        json_return = json.dumps(MockEngine.mock_info_json)
        return HttpResponse(json_return, content_type='application/json')


class ZooniverseEngine(MockEngine):

    def info(self):
        request = urllib2.Request('https://api.zooniverse.org/projects/impossible_line')
        response = urllib2.urlopen(request)
        return HttpResponse(response.read(), content_type='application/json')