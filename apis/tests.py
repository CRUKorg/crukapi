from time import sleep
from django.core.urlresolvers import resolve
from django.test import TestCase, RequestFactory
from django.views.defaults import permission_denied
from apis.controllers import RequestLogController
from apis.models import RequestLogV1, RequestLogV1AttributeValue


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

    def test_can_store_get_dict(self):
        request = RequestFactory().get('test?test_name=test_value')
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 0)
        self.assertEqual(RequestLogV1AttributeValue.objects.all().count(), 0)
        RequestLogController.log_request('test', request)
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 1)
        base_query = RequestLogV1AttributeValue.objects.all()
        self.assertEqual(base_query.count(), 1)
        self.assertEqual(base_query[0].name, "test_name")
        self.assertEqual(base_query[0].value, "test_value")

    def test_can_store_post_dict(self):
        request = RequestFactory().post('test', {'test_name': 'test_value'})
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 0)
        self.assertEqual(RequestLogV1AttributeValue.objects.all().count(), 0)
        RequestLogController.log_request('test', request)
        self.assertEqual(RequestLogV1.objects.filter(project="test", path="/test").count(), 1)
        base_query = RequestLogV1AttributeValue.objects.all()
        self.assertEqual(base_query.count(), 1)
        self.assertEqual(base_query[0].name, "test_name")
        self.assertEqual(base_query[0].value, "test_value")
