from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=100, blank=True, default='')
#     email = models.CharField(max_length=100, blank=True, default='')
#     address = CharField(max_length=100, blank=True, default='')
#     class Meta:
#         ordering = ['created']

# """
# One-to-one relation w/ User
# """
class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)
    line1 = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=200, blank=True, default='')
    state = models.CharField(max_length=20, blank=True, default='')
    zipcode = models.IntegerField()
    class Meta:
        ordering = ['created']