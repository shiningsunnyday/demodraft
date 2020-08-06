from django.db import models

class Politician(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    persona = models.OneToOneField('forward_app.Persona', on_delete=models.CASCADE)
    office_id = models.IntegerField()
    office_name = models.CharField(max_length=200, blank=True, default='')
    fundraised = models.IntegerField(default=0)
    fundraise_goal = models.IntegerField(default=0)
    class Meta:
        ordering = ['created']
