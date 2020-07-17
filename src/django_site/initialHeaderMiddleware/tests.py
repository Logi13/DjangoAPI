from django.conf import settings
from django.template.response import TemplateResponse
from django.test import TestCase

# Create your tests here.
class HeaderTranslationMiddlewareTests(TestCase):
    urls = 'initialHeaderMiddleware.test_urls'

    def test_no_webp(self):
        """
        Test Template response in case of no webp support
        """
        response = self.client.get('/')
        self.assertContains(response, 'script')