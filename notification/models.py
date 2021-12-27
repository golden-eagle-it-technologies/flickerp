from django.db import models
from fauth.models import User


class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, default="Unread")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_read = models.DateField(blank=True, null=True)
