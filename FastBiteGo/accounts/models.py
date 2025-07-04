from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    birthdate = models.PositiveIntegerField(null=True, blank = True)
    address = models.CharField(max_length=40)
    password = models.CharField(max_length=120)
    phone = models.PositiveIntegerField(null = True, blank=True)
    image = models.ImageField(blank=True, null=True)
    courier = models.BooleanField(default=False)

    def __str__(self):
        return self.username

