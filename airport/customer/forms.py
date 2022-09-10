from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from customer.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_type', 'luggage', 'option']


class PassengerForm(ModelForm):

    class Meta:
        model = Passenger
        fields = '__all__'


