from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=500, blank=True)
    avatar = ResizedImageField(size=[1000, None], upload_to='account/avatars/%y/%m/%d', null=True, blank=True)
    token = models.CharField(max_length=124, blank=True)
    balance = models.PositiveIntegerFieldField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Flight(models.Model):
    destination = models.CharField(_("description"), max_length=150, blank=True)
    date_flight = models.DateTimeField(_("date posted"), default=timezone.now)
    tags = models.CharField(_("tags"), max_length=150, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes_post')
    quantity_likes = models.PositiveIntegerField(default=0)


class Ticket(models.Model):
    passenger = models.CharField
    flight = models.ForeignKey()
    check_in = models.BooleanField
    luggage = models.PositiveIntegerField
    option = models.PositiveIntegerField

