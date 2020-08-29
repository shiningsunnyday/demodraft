from django.db import models

# from .politician import Politician, Campaign
from .politician import *
from .policy import *
from .user import *


class Thread(models.Model):
    popularity = models.ForeignKey(
        Popularity,
        on_delete=models.CASCADE,
        null=True
    )
    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.CASCADE,
        null=True
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