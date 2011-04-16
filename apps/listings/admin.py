from django.contrib import admin
from listings.models import Listing, Offer, Comment, Question, Profile

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

class ListingAdmin(admin.ModelAdmin):
    inlines = [OfferInline, QuestionInline,]

class OfferAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]

admin.site.register(Listing, ListingAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Profile)
