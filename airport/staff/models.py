from django.contrib.auth.models import AbstractUser
from django.db import models


class Personal(AbstractUser):
    ROLES_CHOICES = ('Gate manager', 'Check-in manager', 'Supervisor')
    email = models.EmailField(unique=True)
    role = models.Choices(ROLES_CHOICES)
    token = models.CharField(max_length=124, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
