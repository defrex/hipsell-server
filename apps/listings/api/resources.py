from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from listings.api.fields import Base64FileField
from listings.models import Listing, Offer, Comment, Question

class UserResource(ModelResource):
    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        resource_name = 'user'

class ListingResource(ModelResource):
    photo = Base64FileField('photo')
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        queryset = Listing.objects.all()
        resource_name = 'listing'

class OfferResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    listing = fields.ForeignKey(ListingResource, 'listing')

    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        queryset = Offer.objects.all()
        resource_name = 'offer'

class CommentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    offer = fields.ForeignKey(OfferResource, 'offer')

    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        queryset = Comment.objects.all()
        resource_name = 'comment'

class QuestionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    listing = fields.ForeignKey(ListingResource, 'listing')

    class Meta:
        authorization = Authorization()
        queryset = User.objects.all()
        queryset = Question.objects.all()
        resource_name = 'question'
