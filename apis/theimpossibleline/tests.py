from django.core.urlresolvers import resolve
from django.http import HttpResponseNotAllowed
from django.test import TestCase, RequestFactory
from apis.theimpossibleline.views import info


class APIInfoTestCase(TestCase):

    def setUp(self):
        self.url = '/api/projects/impossible_line'

    def test_info_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)

    def test_info_accepts_only_get(self):
        request = RequestFactory().post(self.url)
        response = info(request)
        self.assertTrue(isinstance(response, HttpResponseNotAllowed))
