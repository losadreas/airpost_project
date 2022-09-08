from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Customer(AbstractUser):
    ROLES_CHOICES = (('Gate manager', 'Gate manager'), ('Check-in manager', 'Check-in manager'),
                     ('Supervisor', 'Supervisor'), ('Customer', 'Customer'))
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=124, blank=True)
    balance = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=25, choices=ROLES_CHOICES, default='Customer')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Passenger(models.Model):
    SEX_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    first_name = models.CharField(max_length=48, blank=True)
    last_name = models.CharField(max_length=48, blank=True)
    sex = models.CharField(max_length=12, choices=SEX_CHOICES)
    passport = models.CharField(max_length=16, blank=True)


class Flight(models.Model):
    number = models.CharField(max_length=12, default='NM 12')
    destination = models.CharField(max_length=150, blank=True)
    date_time_flight = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Ticket(models.Model):
    SEAT_CHOICES = (('economy', 'economy'), ('business', 'business'))
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False)
    boarding = models.BooleanField(default=False)
    luggage = models.PositiveIntegerField(default=0)
    option = models.PositiveIntegerField(default=0)
    seat_type = models.CharField(max_length=24, choices=SEAT_CHOICES)


