from django.core.mail import EmailMessage
from airport.settings import DEFAULT_FROM_EMAIL


def create_bill_ticket(passengers, email_customer, flight):
    bill = 0.0
    passengers_info = ''
    flight_info = f'Flight- {flight.number}, {flight.departure}- {flight.destination}, {flight.date_time_flight}'
    AGE_PRICE = {'Adult': 1.0, 'Kid': 0.7, 'Infant': 0.3}
    for passenger in passengers:
        bill += float(flight.price)*AGE_PRICE[passenger.age]
        passengers_info += f'{passenger.first_name}, {passenger.last_name}, {passenger.passport}\n'
    message = f'Your bill - {bill}$ \n passenger(s) - {passengers_info} \n {flight_info}'
    email = EmailMessage('Bill airport', message, from_email=DEFAULT_FROM_EMAIL, to=[email_customer])
    email.send()
