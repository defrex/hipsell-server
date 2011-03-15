from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource

from listings.models import Listing, Location

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'

class ListingResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    location = fields.ForeignKey(LocationResource, 'location')

    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'
