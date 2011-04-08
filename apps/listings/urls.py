from django.conf.urls.defaults import *

from listings.views import ListingView

urlpatterns = patterns('',
    url(r'(?P<id>\d+)/$', ListingView.as_view(), name='listing'),
)