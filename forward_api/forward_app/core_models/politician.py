from django.db import models
from .policy import Policy


class Politician(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    persona = models.OneToOneField('forward_app.Persona', on_delete=models.CASCADE, default=None)
    office_id = models.IntegerField(default=0)  # office_id for what Civic API returns from persona's address
    first = models.CharField(max_length=200, default="")
    last = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200)  # name of office
    approved = models.BooleanField(default=False)  # whether we approved or not, will be returned at login
    policies = models.ManyToManyField(Policy, through='Stance')

    class Meta:
        ordering = ['created']


class Stance(models.Model):
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, default="")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']


class Campaign(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    politician = models.OneToOneField(Politician, on_delete=models.CASCADE, default=None)
    fundraised = models.IntegerField(default=0)
    fundraise_goal = models.IntegerField(default=0)
    actblue = models.URLField(max_length=200, default="")

    class Meta:
        ordering = ['created']