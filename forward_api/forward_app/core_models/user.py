from django.db import models

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, blank=True, default='')
    address = CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']

# """
# One-to-one relation w/ User
# """
class Persona(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']