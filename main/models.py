from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    trial = models.IntegerField(default=0)


class RequestLog(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    request = models.TextField()
    response = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
