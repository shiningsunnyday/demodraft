from django.db import models
from django.contrib.auth.models import User


"""
score function that decides moderator status off Persona data
"""
def score(pers):
    raise NotImplementedError


"""
- periodically, a sweeping operation happens through db that:
        - updates score of every persona
        - calculates top 10 percentile cutoff
        - writes it to /utils/cutoff_history.txt
        - promotes and degrades personas as needed
"""
def sweep():
    raise NotImplementedError


class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="following")
    created = models.DateTimeField(auto_now_add=True)
    num_followers = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)
    score = models.FloatField(default=.0)

    # need to refactor address
    line1 = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=200, blank=True, default='')
    state = models.CharField(max_length=20, blank=True, default='')
    zipcode = models.IntegerField(default=0)

    class Meta:
        ordering = ['created']


class Moderator(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    class Meta:
        ordering = ['created']

