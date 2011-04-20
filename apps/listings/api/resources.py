from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db.models import Max
from tastypie import fields
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.http import HttpCreated
from tastypie.resources import Resource, ModelResource
from tastypie.utils import dict_strip_unicode_keys
from tastypie.validation import FormValidation

from listings.api.authentication import TokenAuthentication
from listings.api.fields import Base64FileField
from listings.forms import UserForm
from listings.models import Listing, Offer, Profile, Comment, Question

class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        allowed_methods = ['post',]
        authentication = Authentication()
        authorization = Authorization()
        fields = ['username', 'token',]
        validation = FormValidation(form_class=UserForm)

    def dehydrate(self, bundle):
        bundle.data['token'] = bundle.obj.profile.token
        return bundle

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(
            request,
            request.raw_post_data,
            format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        updated_bundle = self.obj_create(bundle, request=request)
        resp = self.create_response(request, self.full_dehydrate(updated_bundle.obj))
        resp["location"] = self.get_resource_uri(updated_bundle)
        resp.status_code = 201
        return resp
    
class ListingResource(ModelResource):
    photo = Base64FileField('photo')
    user = fields.ForeignKey(UserResource, 'user')
    offers = fields.ToManyField('listings.api.resources.OfferResource', 'offer_set', full=True, null=True)

    class Meta:
        queryset = Listing.objects.all()
        resource_name = 'listing'

        allowed_methods = ['get', 'post',]
        authentication = TokenAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        offers = bundle.data['offers']
        bundle.data['best_offer'] = offers[0] if offers else None
        del bundle.data['offers']
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = UserResource().get_resource_uri(request.user)
        return super(ListingResource, self).obj_create(bundle, request, **kwargs)


    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        else:
            return super(ListingResource, self).is_authenticated(request, **kwargs)

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
