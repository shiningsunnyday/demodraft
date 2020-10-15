
from django.db import models
from django.contrib.auth.models import User

# """
# One-to-one relation w/ User
# """
class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="following")
    created = models.DateTimeField(auto_now_add=True)
    num_followers = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)
    line1 = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=200, blank=True, default='')
    state = models.CharField(max_length=20, blank=True, default='')
    zipcode = models.IntegerField(default=0)

    score = models.FloatField(default=.0)

    class Meta:
        ordering = ['created']

# class Follow(models.Model):
#     follower = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         null=False
#     )
#     following = models.ForeignKey(
#         Persona,
#         on_delete=models.CASCADE,
#         null=False
#     )

class Following(models.Model):
    user_id = models.IntegerField(default=0)
    persona_id = models.IntegerField(default=0)


