from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    ticket = models.CharField(max_length=500, blank=True)
    token = models.CharField(max_length=124, blank=True)
    balance = models.PositiveIntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Flight(models.Model):
    destination = models.CharField(max_length=150, blank=True)
    date_time_flight = models.DateTimeField(_("date posted"), default=timezone.now)
    tickets = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Ticket(models.Model):
    flight = models.ForeignKey(Flight)
    passenger = models.ForeignKey(Customer)
    price = models.PositiveIntegerField
    check_in = models.BooleanField
    gate
    luggage = models.PositiveIntegerField
    option = models.PositiveIntegerField
    seat_type = models.Choices

class Passenger(models.Model):
    first_name
    last_name
    sex
    passport
