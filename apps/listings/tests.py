import httplib
import base64
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

try:
    import json
except ImportError:
    import simplejson as json

user = User.objects.get(username='jason@hipsell.com')

class UserTestCase(TestCase):
    def test_post_user(self):
        request = HttpRequest()
        post_data = '''{
            "username": "demo@hipsell.com"
            }'''
        request._raw_post_data = post_data
        resp = self.client.post('/api/v1/user/', data=post_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp['location'], 'http://testserver/api/v1/user/3/')
        new_user = User.objects.get(username='demo@hipsell.com')

        # test dupe user posts
        resp = self.client.post('/api/v1/user/', data=post_data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(json.loads(resp.content)['username'][0], 'This email is already registered.')

    def test_login(self):
        token = user.profile.token
        resp = self.client.get('/api/v1/auth/', data={'format': 'json'}, HTTP_AUTHORIZATION='Basic ' + base64.b64encode('jason@hipsell.com:password'))
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['token'], token)

class ListingTestCase(TestCase):
    def test_get_listing_list(self):
        token = user.profile.token
        resp = self.client.get('/api/v1/listing/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized['objects']), 3)
        self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            u'Magic fish hat',
            u'Cat - BNIB',
            u'Slightly used Super 88 system',
        ])
        
    def test_get_listing_detail(self):
        token = user.profile.token
        resp = self.client.get('/api/v1/listing/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        resp = self.client.get('/api/v1/listing/1/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized), 11)
        self.assertEqual(deserialized['description'], u'Slightly used Super 88 system')
        
    def test_get_listing_slice(self):
        token = user.profile.token
        resp = self.client.get('/api/v1/listing/set/2;1/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(len(deserialized), 1)
        self.assertEqual(len(deserialized['objects']), 2)
        self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            u'Cat - BNIB',
            u'Slightly used Super 88 system',
        ])
    
    def test_listing_post(self):
        token = user.profile.token
        request = HttpRequest()
        post_data = '''{
            "description": "Cheap poop", 
            "price": "2", 
            "user": "/api/v1/user/1/",
            "latitude": "43.2", 
            "longtitude": "-79.4",
            "photo": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAATABMDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDpT4yj0rwPDY+KTLeqdZm0LXJhL9o8wyRyOzRNHtITLINuAyLuTbuUVNoWt20ml+DFHjXRtZ1qF1ilNxcJh0lxubYXWTz1QeUjFSxLsGUb2K8L49+IzeI4Tpeh2ktl4eeWVmlSFWN3JvWRJTHs3IPMDtwctkFgM4rktK1m4kkjtlntbiOViTbxySkTr1KmJEc8qOcgjg5rlqYlxdoK51UsOp/E7H13RXknhH4weHdN8MWll4r11o9agaSOdXtLhiAJGCclCT8mzljuP8XOaK6U7q5zNWdjwLxNe3GieLNa0rT5TFZWd/PBBGQH2RrIwVctknAAHJrL/wCEg1T/AJ+v/Ia/4UUVDo03q4r7i1VqL7T+8+mfhT4b0HX/AIb6Zqur6DpV7qF09xJPcT2MTvI3nycklaKKK0SsZt31Z//Z"
            }'''
        request._raw_post_data = post_data
        resp = self.client.post('/api/v1/listing/', data=post_data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp['location'], 'http://testserver/api/v1/listing/4/')

        #make sure posted object exists
        resp = self.client.get('/api/v1/listing/4/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertEqual(obj['description'], 'Cheap poop')

class OfferTestCase(TestCase):
    def test_get_offer_list(self):
        pass
        #token = user.profile.token
        #resp = self.client.get('/api/v1/listing/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        #self.assertEqual(resp.status_code, 200)
        #deserialized = json.loads(resp.content)
        #self.assertEqual(len(deserialized['objects']), 3)
        #self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            #u'Magic fish hat',
            #u'Cat - BNIB',
            #u'Slightly used Super 88 system',
        #])
        
    #def test_get_listing_detail(self):
        #token = user.profile.token
        #resp = self.client.get('/api/v1/listing/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        #resp = self.client.get('/api/v1/listing/1/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        #self.assertEqual(resp.status_code, 200)
        #deserialized = json.loads(resp.content)
        #self.assertEqual(len(deserialized), 11)
        #self.assertEqual(deserialized['description'], u'Slightly used Super 88 system')
        
    #def test_get_listing_slice(self):
        #token = user.profile.token
        #resp = self.client.get('/api/v1/listing/set/2;1/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        #self.assertEqual(resp.status_code, 200)
        #deserialized = json.loads(resp.content)
        #self.assertEqual(len(deserialized), 1)
        #self.assertEqual(len(deserialized['objects']), 2)
        #self.assertEqual([obj['description'] for obj in deserialized['objects']], [
            #u'Cat - BNIB',
            #u'Slightly used Super 88 system',
        #])
    
    #def test_listing_post(self):
        #token = user.profile.token
        #request = HttpRequest()
        #post_data = '''{
            #"description": "Cheap poop", 
            #"price": "2", 
            #"user": "/api/v1/user/1/",
            #"latitude": "43.2", 
            #"longtitude": "-79.4",
            #"photo": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAATABMDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDpT4yj0rwPDY+KTLeqdZm0LXJhL9o8wyRyOzRNHtITLINuAyLuTbuUVNoWt20ml+DFHjXRtZ1qF1ilNxcJh0lxubYXWTz1QeUjFSxLsGUb2K8L49+IzeI4Tpeh2ktl4eeWVmlSFWN3JvWRJTHs3IPMDtwctkFgM4rktK1m4kkjtlntbiOViTbxySkTr1KmJEc8qOcgjg5rlqYlxdoK51UsOp/E7H13RXknhH4weHdN8MWll4r11o9agaSOdXtLhiAJGCclCT8mzljuP8XOaK6U7q5zNWdjwLxNe3GieLNa0rT5TFZWd/PBBGQH2RrIwVctknAAHJrL/wCEg1T/AJ+v/Ia/4UUVDo03q4r7i1VqL7T+8+mfhT4b0HX/AIb6Zqur6DpV7qF09xJPcT2MTvI3nycklaKKK0SsZt31Z//Z"
            #}'''
        #request._raw_post_data = post_data
        #resp = self.client.post('/api/v1/listing/', data=post_data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + token)
        #self.assertEqual(resp.status_code, 201)
        #self.assertEqual(resp['location'], 'http://testserver/api/v1/listing/4/')

        ##make sure posted object exists
        #resp = self.client.get('/api/v1/listing/4/', data={'format': 'json'}, HTTP_AUTHORIZATION='Token ' + token)
        #self.assertEqual(resp.status_code, 200)
        #obj = json.loads(resp.content)
        #self.assertEqual(obj['description'], 'Cheap poop')
