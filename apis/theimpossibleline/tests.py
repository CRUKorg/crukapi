import json
import types
from django.core.urlresolvers import resolve
from django.http import HttpResponseNotAllowed
from django.test import TestCase, RequestFactory
from apis.theimpossibleline.engines import EngineFactory, ZooniverseEngine, MockEngine
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

    def test_mock_info_returns_valid_json(self):
        request = RequestFactory().get(self.url)
        response = info(request)
        self.assertEqual(response.content, json.dumps(MockEngine.mock_info_json))


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

    def test_engine_has_info_method(self):
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="ZooniverseEngine"):
            engine = EngineFactory.get_engine(None)
            self.assertTrue(hasattr(engine, 'info'))
            self.assertEqual(type(getattr(engine, 'info')), types.MethodType)

    def test_request_is_passed_to_engine(self):
        request = "this is a dummy request object"
        with self.settings(API_IMPOSSIBLE_LINE_ENGINE="ZooniverseEngine"):
            engine = EngineFactory.get_engine(request)
            self.assertEqual(request, engine.request)

