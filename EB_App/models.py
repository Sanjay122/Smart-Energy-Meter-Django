from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    role = models.CharField(max_length=120)
    authorities = models.CharField(max_length=120)
    isEnabled = models.BooleanField()
    
