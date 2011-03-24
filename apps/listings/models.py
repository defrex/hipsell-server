from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id',]

class Location(BaseModel):
    """
    Coordinate location.
    """
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longtitude = models.DecimalField(max_digits=7, decimal_places=4)

    def __unicode__(self):
        return '%s, %s' % (self.latitude, self.longtitude,)

class Listing(BaseModel):
    """
    Seller's listing.
    """
    description = models.CharField(max_length=255)
    location = models.OneToOneField(Location, null=True, blank=True)
    photo = models.ImageField(upload_to='uploads', null=True, blank=True)
    user = models.ForeignKey(User)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return self.description

class Offer(BaseModel):
    """
    Potential buyer's offer on a listing.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User)
    listing = models.ForeignKey(Listing)

    def __unicode__(self):
        return '$%d' % (self.amount,)

class Comment(BaseModel):
    """
    Conversation over an offer.
    """
    comment = models.TextField()
    offer = models.ForeignKey(Offer)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.comment

class Question(BaseModel):
    """
    Pre-sale questions and answers (public).
    """
    answer = models.TextField(blank=True)
    listing = models.ForeignKey(Listing)
    user = models.ForeignKey(User)
    question = models.CharField(max_length=255)

    def __unicode__(self):
        return self.question
