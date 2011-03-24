from django.contrib import admin

from listings.models import Listing, Offer, Comment, Question

admin.site.register(Listing)
admin.site.register(Offer)
admin.site.register(Comment)
admin.site.register(Question)
