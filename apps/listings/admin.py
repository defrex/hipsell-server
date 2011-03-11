from django.contrib import admin

from listings.models import Location, Listing, Offer, Comment, Question

admin.site.register(Location)
admin.site.register(Listing)
admin.site.register(Offer)
admin.site.register(Comment)
admin.site.register(Question)
