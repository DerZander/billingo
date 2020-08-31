from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    birthday = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    housenumber = models.CharField(max_length=250, null=True, blank=True)
    postcode = models.CharField(max_length=5, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)

    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.username


