from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Auto-generate token for every user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# """
# One-to-one relation w/ User
# """
class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="following")
    created = models.DateTimeField(auto_now_add=True)
    num_followers = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)
    line1 = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=200, blank=True, default='')
    state = models.CharField(max_length=20, blank=True, default='')
    zipcode = models.IntegerField(default=0)

    score = models.FloatField(default=.0)

    class Meta:
        ordering = ['created']


