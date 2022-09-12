from django.core.mail import EmailMessage
from airport.settings import DEFAULT_FROM_EMAIL


def create_bill(price, quantity_passenger, email_customer):
    message = f'Your bill - {price*quantity_passenger}'
    email = EmailMessage('Bill airport', message, from_email=DEFAULT_FROM_EMAIL, to=[email_customer])
    email.send()
