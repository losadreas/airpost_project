from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from customer.models import Customer, Flight


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']


class FlightForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['destination', 'date_time_flight']

