import json
import sys
import urllib
import urllib2
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed


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

    mock_status_json = {
        'random': 0.4766550899055938, 
        'classification_count': 85, 
        'created_at': '2014-07-14T15:41:24Z',
        'updated_at': '2014-07-14T15:41:24Z',
        'state': 'active',
        'zooniverse_id': 'AIL000000x', 
        'coords': [],
        'location': {
            'standard': 'http://www.generunner.net.s3-website-us-east-1.amazonaws.com/subjects/standard/52e42e8806715edea2000055.txt'},
        'workflow_ids': ['53c3e9090ab4c05d28000002'],
        'project_id': '53c3e9090ab4c05d28000001',
        'id': '53c3f861eec846061b000021',
        'metadata': {
            'file_name': 'MB-0006Chrom3.txt',
            'gene_runner_id': '52e42e8806715edea2000055'
        }}

    def __init__(self, request):
        self.request = request

    def proxy(self):
        json_return = json.dumps(MockEngine.mock_info_json)
        return HttpResponse(json_return, content_type='application/json')


class ZooniverseEngine(MockEngine):

    def proxy(self):
        if self.request.method == "GET":
            request = urllib2.Request(
                'https://api.zooniverse.org%s?%s' % (
                    ''.join(self.request.path[4:]),
                    '&'.join(["%s=%s" % (k, v) for k, v in self.request.GET.items()])))
        elif self.request.method == "POST":
            request = urllib2.Request(
                'https://api.zooniverse.org%s' % ''.join(self.request.path[4:]),
                urllib.urlencode(self.request.POST))
        else:
            return HttpResponseNotAllowed(["GET", "POST"])
        response = urllib2.urlopen(request)
        return HttpResponse(response.read(), content_type='application/json')