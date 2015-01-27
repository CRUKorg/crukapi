from django.core.urlresolvers import resolve
from django.test import TestCase
from django.views.defaults import permission_denied


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
