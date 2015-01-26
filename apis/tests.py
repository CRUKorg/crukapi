from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase, RequestFactory
from django.views.defaults import permission_denied


class BaseAPITestCase(TestCase):

    def test_empty_path_returns_403(self):
        self.assertRaises(NoReverseMatch, reverse, '/')