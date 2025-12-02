from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

# Create your tests here.


class TestService(TestCase):
    def test_service(self):
        self.assertEqual(settings.FOO, "FOO override from apps/api")
        self.assertTrue(True)

    @override_settings(FOO="new value")
    def test_with_overriden_settings(self):
        self.assertEqual(settings.FOO, "new value")

    def test_url_loading(self):
        expected = "/api/nothing"
        reversed = reverse("api:nothing")
        self.assertEqual(reversed, expected)
