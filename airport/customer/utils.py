from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from airport.settings import DEFAULT_FROM_EMAIL
from customer.models import Ticket
import datetime


def create_bill_ticket(passengers, email_customer, flight):
    bill = 0.0
    passengers_info = ''
    flight_info = f'Flight- {flight.number}, {flight.departure}- {flight.destination}, ' \
                  f'{flight.date_time_flight:%Y-%m-%d %H:%M}'
    AGE_RATE = {'Adult': 1.0, 'Kid': 0.7, 'Infant': 0.3, 'luggage': 0.1}
    for passenger in passengers:
        ticket = Ticket.objects.get(passenger=passenger)
        bill += float(flight.price) * AGE_RATE[ticket.age_type]
        bill += float(flight.price) * ticket.luggage * AGE_RATE['luggage']
        passengers_info += f'{passenger.first_name} {passenger.last_name}\n {passenger.passport},' \
                           f' {ticket.age_type}, {passenger.sex}, {ticket.luggage}\n '
    message = f'Your bill - {round(bill,2)}$ \n passenger(s) - {passengers_info} \n {flight_info}'
    email = EmailMessage('Bill airport', message, from_email=DEFAULT_FROM_EMAIL, to=[email_customer])
    email.send()
    return message


def calculate_age(passenger, flight):
    age = flight.date_time_flight.date() - passenger.date_birth
    if age < datetime.timedelta(days=2 * 365):
        age_type = 'Infant'
    elif age < datetime.timedelta(days=12 * 365):
        age_type = 'Kid'
    else:
        age_type = 'Adult'
    return age_type


def send_email_verify(host, token, customer_pk, email):
    message = f'Verify email Follow the link {host}/customers/verify_email/{token}/{str(urlsafe_base64_encode(force_bytes(customer_pk)))}/'
    email = EmailMessage('Verify email', message, from_email=DEFAULT_FROM_EMAIL, to=[email])
    email.send()
