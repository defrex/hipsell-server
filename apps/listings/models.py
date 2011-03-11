from django.contrib.auth.models import User
from django.db import models

class Location(models.Model):
    """
    Coordinate location.
    """
    latitude = models.IntegerField()
    longtitude = models.IntegerField()

    def __unicode__(self):
        return '%s, %s' % (self.latitude, self.longtitude,)

class Listing(models.Model):
    """
    Seller's listing.
    """
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    location = models.OneToOneField(Location)
    photo = models.ImageField(upload_to='foo')
    poster = models.ForeignKey(User)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return self.description

class Offer(models.Model):
    """
    Potential buyer's offer on a listing.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    poster = models.ForeignKey(User)
    listing = models.ForeignKey(Listing)

    def __unicode__(self):
        return '$%d' % (self.amount,)

class Comment(models.Model):
    """
    Conversation over an offer.
    """
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(Offer)
    poster = models.ForeignKey(User)

    def __unicode__(self):
        return self.comment

class Question(models.Model):
    """
    Pre-sale questions and answers (public).
    """
    answer = models.TextField(blank=True)
    listing = models.ForeignKey(Listing)
    poster = models.ForeignKey(User)
    question = models.CharField(max_length=255)

    def __unicode__(self):
        return self.question
