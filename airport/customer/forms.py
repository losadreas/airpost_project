from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from customer.models import Customer, Ticket


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_type', 'price', 'luggage', 'option']

