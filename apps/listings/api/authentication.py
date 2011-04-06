from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class TokenAuthentication(Authentication):

    def _unauthorized(self):
        return HttpUnauthorized()

    def is_authenticated(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()
        
        try:
            (auth_type, token) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type != 'Token':
                return self._unauthorized()
        except:
            return self._unauthorized()

        try:
            user = User.objects.get(profile__token=token)
        except User.DoesNotExist:
            return self._unauthorized()

        request.user = user

        return True
    
    def get_identifier(self, request):
        # TODO wtf is this nerd shit
        return request.META.get('REMOTE_USER', 'nouser')
