from django.db import models
from django.contrib.auth.models import User

"""
Many-to-many relation w/ User
"""
class Policy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField() 
    name = models.CharField(max_length=100, blank=True, default='')
    statement = models.CharField(max_length=500, blank=True, default='')
    description = models.TextField(blank=True, default='')
    class Meta:
        ordering = ['created']



class Popularity(models.Model):
    policy = models.OneToOneField(
        Policy,
        on_delete=models.CASCADE,
        primary_key=True
    )
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    class Meta:
        ordering = ['created']



class Thread(models.Model):
    popularity = models.ForeignKey(
        Popularity,
        on_delete=models.CASCADE
    )
    lead_comment_id = models.IntegerField(default=0)



class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    next_comment_id = models.IntegerField(default=0)
    content = models.CharField(max_length=1000, blank=True, default='')
    likes = models.IntegerField(default=0)
    class Meta:
        ordering = ['time']


