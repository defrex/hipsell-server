import random
from django.contrib.auth.models import User, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.hashcompat import sha_constructor

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-id',]

class Profile(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created: 
        basic_group, created = Group.objects.get_or_create(name='basic')
        if created:
            basic_group.permissions.add(Permission.objects.get(codename='add_listing'))
            basic_group.permissions.add(Permission.objects.get(codename='add_offer'))
            basic_group.permissions.add(Permission.objects.get(codename='add_question'))
        instance.groups.add(basic_group)
        instance.save()
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        token = sha_constructor(salt+instance.username).hexdigest()
        Profile.objects.create(user=instance, token=token)

class Listing(BaseModel):
    """
    Seller's listing.
    """
    description = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='uploads', null=True, blank=True)
    user = models.ForeignKey(User)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.description
    
    def best_offer(self):
        return Offer.objects.filter(listing=self).order_by('-amount')[0]

class Offer(BaseModel):
    """
    Potential buyer's offer on a listing.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User)
    listing = models.ForeignKey(Listing)

    class Meta:
        ordering = ['-amount',]

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
