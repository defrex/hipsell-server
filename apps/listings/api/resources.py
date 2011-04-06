from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.http import HttpCreated
from tastypie.resources import ModelResource
from tastypie.utils import dict_strip_unicode_keys

from listings.api.authentication import TokenAuthentication
from listings.api.fields import Base64FileField
from listings.models import Listing, Offer, Profile, Comment, Question

class UserResource(ModelResource):
    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        allowed_methods = ['post',]
        authentication = Authentication()
        authorization = Authorization()

class ListingResource(ModelResource):
    photo = Base64FileField('photo')
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'

        authentication = TokenAuthentication()
        authorization = DjangoAuthorization()

class OfferResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    listing = fields.ForeignKey(ListingResource, 'listing')

    class Meta:
        queryset = Offer.objects.all()
        resource_name = 'offer'

        authentication = TokenAuthentication()
        authorization = DjangoAuthorization()

class CommentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    offer = fields.ForeignKey(OfferResource, 'offer')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'

        authentication = TokenAuthentication()
        authorization = DjangoAuthorization()

class QuestionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    listing = fields.ForeignKey(ListingResource, 'listing')

    class Meta:
        queryset = Question.objects.all()
        resource_name = 'question'

        authentication = TokenAuthentication()
        authorization = DjangoAuthorization()
