from django.db import models
# from .user import User

class Politician(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']

"""
Can destroy current db.sqlite3 before migrating new Politician model
Many-to-many relation w/ User
"""
# class Politician(models.Model):
#     class Meta:
#
#
# """
# One-to-one relation w/ Politician
# """
# class Campaign(models.Model):
#     class Meta:
