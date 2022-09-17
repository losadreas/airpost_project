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
        fields = ['seat_type', 'luggage', 'option']


class PassengerForm(ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        birth_date = self.cleaned_data['date_birth']
        now_date = date.today()
        print(birth_date, now_date)
        if birth_date > now_date:
            print('raise')
            raise forms.ValidationError("Please, check the date of birth")
        # return super(PassengerForm, self).clean()

    class Meta:
        model = Passenger
        fields = '__all__'


class QuantityPassengerForm(forms.Form):
    quantity_passenger = forms.IntegerField(label='Quantity Passengers', min_value=1, max_value=24)
