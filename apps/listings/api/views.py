import base64
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

def auth(request):
    try:
        auth_type, data = request.META['HTTP_AUTHORIZATION'].split()
        user_pass = base64.b64decode(data).split(':')
        user = authenticate(username=user_pass[0], password=user_pass[1])
        return HttpResponse(json.dumps({'token': user.profile.token}), mimetype='application/json')
    except:
        return HttpResponse('Unauthorized', status=401)
