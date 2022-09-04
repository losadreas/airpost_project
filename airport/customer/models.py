from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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
    date_time_flight = models.DateTimeField(default=timezone.now)
    tickets = models.ForeignKey


class Ticket(models.Model):
    flight = models.ForeignKey(Flight)
    passenger = models.ForeignKey(Customer)
    price = models.PositiveIntegerField
    check_in = models.BooleanField
    boarding = models.BooleanField
    luggage = models.PositiveIntegerField
    option = models.PositiveIntegerField
    seat_type = models.Choices


class Passenger(models.Model):
    first_name = models.CharField
    last_name = models.CharField
    sex = models.Choices
    passport = models.CharField
