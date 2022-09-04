from django.contrib.auth.forms import UserCreationForm
from customer.models import Customer


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']
