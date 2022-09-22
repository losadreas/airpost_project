from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from customer.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_type', 'luggage']


class PassengerForm(ModelForm):
    def clean_date_birth(self):
        birth_date = self.cleaned_data['date_birth']
        now_date = date.today()
        if birth_date > now_date:
            raise forms.ValidationError("Please, check the date of birth")
        return birth_date

    class Meta:
        model = Passenger
        fields = '__all__'


class QuantityPassengerForm(forms.Form):
    quantity_passenger = forms.IntegerField(label='Quantity Passengers', min_value=1, max_value=24)


