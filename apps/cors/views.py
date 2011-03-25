
from django.http import HttpResponse

def cors_test(request):
    return HttpResponse('{"key": "value"}', mimetype='application/json')
