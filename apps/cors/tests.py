
from django.test import TestCase
from django.test.client import Client

class CorsTest(TestCase):
    def test_cors_request(self):
        """
        Test that the appropriate headers are set.
        """
        c = Client()
        resp = c.post('/', content_type='application.json', Origin='http://example.com')

        self.assertEqual(resp['Access-Control-Allow-Origin'], '*')
        self.assertEqual(resp['Access-Control-Allow-Methods'], 'GET, POST, PUT, DELETE')
        self.assertEqual(resp['Access-Control-Allow-Credentials'], 'true')



