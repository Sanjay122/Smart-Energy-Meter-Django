from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    role = models.CharField(max_length=120)
    authorities = models.CharField(max_length=120)
    isEnabled = models.BooleanField()

    def __str__(self):
        return self.user.username + '  ' + self.role


class Consumer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    supply_phase = models.IntegerField()
    door_number = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    post_office = models.CharField(max_length=120)
    taluk = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    pin_number = models.IntegerField()
    eb_number = models.CharField(max_length=14)

    def __str__(self):
        return self.account.user.username
