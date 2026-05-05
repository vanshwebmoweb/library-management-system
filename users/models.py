from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True,)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True,)

    def __str__(self):
        return self.username
