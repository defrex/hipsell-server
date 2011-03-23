from django.http import HttpRequest
from django.test import TestCase
try:
    import json
except ImportError:
    import simplejson as json

class ViewsTestCase(TestCase):

    def test_gets(self):
        resp = self.client.get('/api/v1/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized), 6)
        self.assertEqual(deserialized['listing'], {'list_endpoint': '/api/v1/listing/', 'schema': '/api/v1/listing/schema/'})
        
        resp = self.client.get('/api/v1/listing/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 3)
        self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            u'Magic fish hat',
            u'Cat - BNIB',
            u'Slightly used Super 88 system',
        ])
        
        resp = self.client.get('/api/v1/listing/1/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized), 10)
        self.assertEqual(deserialized['description'], u'Slightly used Super 88 system')
        
        resp = self.client.get('/api/v1/listing/set/2;1/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized), 1)
        self.assertEqual(len(deserialized['objects']), 2)
        self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            u'Cat - BNIB',
            u'Slightly used Super 88 system',
        ])
    
    def test_posts(self):
        request = HttpRequest()
        post_data = '''{
            'description': 'Slightly used Super 88 system', 
            'photo': 'uploads/7725.mariotwins.jpg', 
            'price': '2', 
            'user': '/api/v1/users/1/',
            'location': '/api/v1/location/1/',
        }'''
        request._raw_post_data = post_data
        
        resp = self.client.post('/api/v1/listing/', data=post_data, content_type='application/json')
        print resp
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp['location'], 'http://testserver/api/v1/listing/4/')

        #make sure posted object exists
        resp = self.client.get('/api/v1/listing/4/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertEqual(obj['description'], 'Slightly used Super 88 system')
    
    #def test_api_field_error(self):
        ## When a field error is encountered, we should be presenting the message
        ## back to the user.
        #request = HttpRequest()
        #post_data = '{"content": "More internet memes.", "is_active": true, "title": "IT\'S OVER 9000!", "slug": "its-over", "user": "/api/v1/users/9001/"}'
        #request._raw_post_data = post_data
        
        #resp = self.client.post('/api/v1/notes/', data=post_data, content_type='application/json')
        #self.assertEqual(resp.status_code, 400)
        #self.assertEqual(resp.content, "Could not find the provided object via resource URI '/api/v1/users/9001/'.")


    #def test_options(self):
        #resp = self.client.options('/api/v1/notes/')
        #self.assertEqual(resp.status_code, 200)
        #allows = 'GET,POST,PUT,DELETE'
        #self.assertEqual(resp['Allow'], allows)
        #self.assertEqual(resp.content, allows)

        #resp = self.client.options('/api/v1/notes/1/')
        #self.assertEqual(resp.status_code, 200)
        #allows = 'GET,POST,PUT,DELETE'
        #self.assertEqual(resp['Allow'], allows)
        #self.assertEqual(resp.content, allows)

        #resp = self.client.options('/api/v1/notes/schema/')
        #self.assertEqual(resp.status_code, 200)
        #allows = 'GET'
        #self.assertEqual(resp['Allow'], allows)
        #self.assertEqual(resp.content, allows)

        #resp = self.client.options('/api/v1/notes/set/2;1/')
        #self.assertEqual(resp.status_code, 200)
        #allows = 'GET'
        #self.assertEqual(resp['Allow'], allows)
        #self.assertEqual(resp.content, allows)

#from tests.testcases import TestServerTestCase
#import httplib
#try:
    #import json
#except ImportError:
    #import simplejson as json


#class HTTPTestCase(TestServerTestCase):
    #def setUp(self):
        #self.start_test_server(address='localhost', port=8001)

    #def tearDown(self):
        #self.stop_test_server()

    #def get_connection(self):
        #return httplib.HTTPConnection('localhost', 8001)

    #def test_get_apis_json(self):
        #connection = self.get_connection()
        #connection.request('GET', '/api/v1/', headers={'Accept': 'application/json'})
        #response = connection.getresponse()
        #connection.close()
        #data = response.read()
        #self.assertEqual(response.status, 200)
        #self.assertEqual(data, '{"notes": {"list_endpoint": "/api/v1/notes/", "schema": "/api/v1/notes/schema/"}, "users": {"list_endpoint": "/api/v1/users/", "schema": "/api/v1/users/schema/"}}')

    #def test_get_apis_xml(self):
        #connection = self.get_connection()
        #connection.request('GET', '/api/v1/', headers={'Accept': 'application/xml'})
        #response = connection.getresponse()
        #connection.close()
        #data = response.read()
        #self.assertEqual(response.status, 200)
        #self.assertEqual(data, '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<response><notes type="hash"><list_endpoint>/api/v1/notes/</list_endpoint><schema>/api/v1/notes/schema/</schema></notes><users type="hash"><list_endpoint>/api/v1/users/</list_endpoint><schema>/api/v1/users/schema/</schema></users></response>')

    #def test_get_list(self):
        #connection = self.get_connection()
        #connection.request('GET', '/api/v1/notes/', headers={'Accept': 'application/json'})
        #response = connection.getresponse()
        #connection.close()
        #self.assertEqual(response.status, 200)
        #self.assertEqual(response.read(), '{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 2}, "objects": [{"content": "This is my very first post using my shiny new API. Pretty sweet, huh?", "created": "2010-03-30T20:05:00", "id": "1", "is_active": true, "resource_uri": "/api/v1/notes/1/", "slug": "first-post", "title": "First Post!", "updated": "2010-03-30T20:05:00", "user": "/api/v1/users/1/"}, {"content": "The dog ate my cat today. He looks seriously uncomfortable.", "created": "2010-03-31T20:05:00", "id": "2", "is_active": true, "resource_uri": "/api/v1/notes/2/", "slug": "another-post", "title": "Another Post", "updated": "2010-03-31T20:05:00", "user": "/api/v1/users/1/"}]}')

    #def test_post_object(self):
        #connection = self.get_connection()
        #post_data = '{"content": "A new post.", "is_active": true, "title": "New Title", "slug": "new-title", "user": "/api/v1/users/1/"}'
        #connection.request('POST', '/api/v1/notes/', body=post_data, headers={'Accept': 'application/json', 'Content-type': 'application/json'})
        #response = connection.getresponse()
        #self.assertEqual(response.status, 201)
        #self.assertEqual(dict(response.getheaders())['location'], 'http://localhost:8001/api/v1/notes/3/')

        ## make sure posted object exists
        #connection.request('GET', '/api/v1/notes/3/', headers={'Accept': 'application/json'})
        #response = connection.getresponse()
        #connection.close()

        #self.assertEqual(response.status, 200)

        #data = response.read()
        #obj = json.loads(data)

        #self.assertEqual(obj['content'], 'A new post.')
        #self.assertEqual(obj['is_active'], True)
        #self.assertEqual(obj['user'], '/api/v1/users/1/')

