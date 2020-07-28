from django.db import models
from django.contrib.auth.models import User

# """
# One-to-one relation w/ User
# """
class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']