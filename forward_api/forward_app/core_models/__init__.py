from django.db import models

# from .politician import Politician, Campaign
from .politician import *
from .policy import *
from .user import Persona


"""
Can define intermediate models for many-to-many relations here
"""

"""
Intermediate model for Politician - Policy
"""
# class Stance(models.Model):
#     class Meta:
