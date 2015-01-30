from time import sleep
from django.core.urlresolvers import resolve
from django.test import TestCase, RequestFactory
from django.views.defaults import permission_denied
from apis.controllers import RequestLogController
from apis.models import RequestLogV1


class BaseAPITestCase(TestCase):

    def test_empty_path_returns_403(self):
        view = resolve('/')
        self.assertEqual(view.func, permission_denied)

    def test_empty_api_path_returns_403(self):
        view = resolve('/api')
        self.assertEqual(view.func, permission_denied)

    def test_empty_api_projects_path_returns_403(self):
        view = resolve('/api/projects')
        self.assertEqual(view.func, permission_denied)


class RequestLogControllerTestCase(TestCase):

    def test_log_request(self):
        request = RequestFactory().get('test')
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 0)
        RequestLogController.log_request('test', request)
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 1)
