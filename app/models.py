from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    full_date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Event_User(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
