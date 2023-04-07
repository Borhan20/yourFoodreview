from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class UserMessage(models.Model):
    message = models.CharField(max_length=500)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    date_messaged = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_messaged']


    def __str__(self):
        return self.message