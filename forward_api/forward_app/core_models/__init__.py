from django.db import models

# from .politician import Politician, Campaign
from .politician import Politician
# from .policy import Policy, Popularity, Comment
from .user import User, Persona


"""
Can define intermediate models for many-to-many relations here
"""

"""
Intermediate model for Politician - Policy
"""
# class Stance(models.Model):
#     class Meta: