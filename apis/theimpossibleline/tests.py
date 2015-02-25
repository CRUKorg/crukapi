from copy import copy
import json
import types
from django.core.urlresolvers import resolve
from django.http import HttpResponseNotAllowed
from django.test import TestCase, RequestFactory
from apis.theimpossibleline.engines import EngineFactory, ZooniverseEngine, MockEngine
from apis.theimpossibleline.views import proxy


class APIInfoTestCase(TestCase):

    def setUp(self):
        self.url = '/api/projects/impossible_line'

    def test_info_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)
        self.assertEqual(view.func, proxy)

    def test_mock_info_returns_valid_json(self):
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="MockEngine"):
            request = RequestFactory().get(self.url)
            response = proxy(request)
            self.assertEqual(response.content, json.dumps(MockEngine.mock_info_json))

    def test_info_returns_valid_json_but_not_mock(self):
        request = RequestFactory().get(self.url)
        response = proxy(request)
        self.assertNotEqual(response.content, json.dumps(MockEngine.mock_info_json))
        response_object = json.loads(response.content)
        for attr in MockEngine.mock_info_json.keys():
            self.assertIn(attr, response_object)


class APISubjectsTestCase(TestCase):

    def setUp(self):
        self.url = "/api/projects/impossible_line/subjects?limit=1"

    def test_subjects_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)
        self.assertEqual(view.func, proxy)

    def test_subjects_returns_valid(self):
        request = RequestFactory().get(self.url)
        response = proxy(request)
        response_object = json.loads(response.content)
        self.assertTrue(isinstance(response_object, list))
        self.assertTrue(len(response_object), 1)
        obj = response_object[0]
        for attr in MockEngine.mock_status_json.keys():
            self.assertIn(attr, obj)

    def test_get_variables_are_passed(self):
        url = copy(self.url)
        url = url.replace('limit=1', 'limit=2')
        request = RequestFactory().get(url)
        response = proxy(request)
        response_object = json.loads(response.content)
        self.assertTrue(isinstance(response_object, list))
        self.assertEqual(len(response_object), 2)


class APISignupTestCase(TestCase):

    def setUp(self):
        self.url = "/api/projects/impossible_line/signup"

    def test_signup_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)
        self.assertEqual(view.func, proxy)

    def test_proxy_with_no_post_variables(self):
        request = RequestFactory().post(self.url, {})
        response = proxy(request)
        response_object = json.loads(response.content)
        self.assertIn("success", response_object)
        self.assertFalse(response_object['success'])
        self.assertTrue("Login can't be blank" in response_object['message'])

    def test_proxy_can_pass_post_variable(self):
        data = {'username': 'test', 'password': 'test', 'email': 'test@test.com', 'real_name': 'test'}
        request = RequestFactory().post(self.url, data)
        response = proxy(request)
        response_object = json.loads(response.content)
        self.assertIn("success", response_object)
        self.assertFalse(response_object['success'])
        self.assertTrue("Login has already been taken" in response_object['message'])


class APILoginTestCase(TestCase):

    def setUp(self):
        self.url = "/api/projects/impossible_line/login"

    def test_login_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)
        self.assertEqual(view.func, proxy)


class APIClassificationTestCase(TestCase):

    def setUp(self):
        self.url = "/api/projects/impossible_line/workflows/fdf78d87f8d7fd/classifications"

    def test_classification_url(self):
        view = resolve(self.url)
        self.assertIsNotNone(view)
        self.assertEqual(view.func, proxy)


class EngineFactoryTestCase(TestCase):

    def test_returns_zooniverse_engine_by_default(self):
        engine = EngineFactory.get_engine(None)
        self.assertTrue(isinstance(engine, ZooniverseEngine))

    def test_can_return_mock_engine(self):
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="MockEngine"):
            engine = EngineFactory.get_engine(None)
            self.assertFalse(isinstance(engine, ZooniverseEngine))
            self.assertTrue(isinstance(engine, MockEngine))


class ZooniverseEngineTestCase(TestCase):

    def test_engine_has_proxy_method(self):
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="ZooniverseEngine"):
            engine = EngineFactory.get_engine(None)
            self.assertTrue(hasattr(engine, 'proxy'))
            self.assertEqual(type(getattr(engine, 'proxy')), types.MethodType)

    def test_request_is_passed_to_engine(self):
        request = "this is a dummy request object"
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="ZooniverseEngine"):
            engine = EngineFactory.get_engine(request)
            self.assertEqual(request, engine.request)

