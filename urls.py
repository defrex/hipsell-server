from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api

from listings.api.resources import *

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ListingResource())
v1_api.register(OfferResource())
v1_api.register(CommentResource())
v1_api.register(QuestionResource())

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/v1/auth/', 'listings.api.views.auth'),
    (r'^api/', include(v1_api.urls)),
    (r'^listings/', include('listings.urls')),
    (r'^test/$', direct_to_template, {'template': 'test.html'}),
    (r'^cors_test/$', 'cors.views.cors_test'),
    (r'^/?$', direct_to_template, {'template': 'base.html'}),
)

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                    {'document_root': settings.MEDIA_ROOT}),
    )
