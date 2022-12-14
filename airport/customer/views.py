from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from customer.forms import *
from customer.models import Ticket, Passenger, Flight
from django.forms import formset_factory
from customer.utils import create_bill_ticket, calculate_age, send_email_verify

Customer = get_user_model()


class HomeView(View):
    def get(self, request):
        template = "home.html"
        return render(request, template)


class ConfirmEmail(View):
    def get(self, request):
        template = "confirm_email.html"
        return render(request, template)


class CheckLink(View):
    def get(self, request):
        template = "check_link.html"
        return render(request, template)


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            customer = Customer.objects.get(email=request.POST.get("email"))
            account_activation_token = PasswordResetTokenGenerator()
            customer.token = account_activation_token.make_token(customer)
            customer.is_active = False
            customer.save()
            send_email_verify(request._current_scheme_host, customer.token, customer.pk, customer.email)
            return redirect('confirm_email')
        context = {'form': form}
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        logout(request)
        result = super(SignUp, self).get(request, *args, **kwargs)
        return result


class VerifyEmail(View):
    template_name = 'verify_email.html'

    def get(self, request, token, pk_code):
        customer = Customer.objects.get(pk=urlsafe_base64_decode(pk_code).decode())
        if customer.token == token:
            customer.is_active = True
            customer.save()
            login(request, customer, backend='django.contrib.auth.backends.ModelBackend')
        else:
            return redirect('check_link')
        return redirect('customer_cabinet')


class LogOut(View):
    def get(self, request):
        logout(request)
        template = 'logout.html'
        return render(request, template)


class CustomerCabinet(View):
    def get(self, request):
        if request.user.id is None:
            return redirect('login')
        template = 'customer_cabinet.html'
        tickets = Ticket.objects.filter(customer=request.user).all()
        customer = Customer.objects.get(id=request.user.id)
        return render(request, template, {'customer': customer, 'tickets': tickets})


class FlightView(CreateView):
    def get(self, request):
        if request.user.id is None:
            return redirect('login')
        flights = Flight.objects.all()
        template = "flight.html"
        return render(request, template, {'flights': flights})


class BookTicketView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "book_ticket.html"

    def get(self, request):
        form = TicketForm()
        passengers = Passenger.objects.filter(pk__in=request.session.get('booked_passengers')).all()
        flight = Flight.objects.get(pk=request.session.get('flight_pk'))
        return render(request, 'book_ticket.html', {'flight': flight, 'form': form, 'passengers': passengers})

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST, instance=request.user)
        passengers = Passenger.objects.filter(pk__in=request.session.get('booked_passengers')).all()
        flight = Flight.objects.get(pk=request.session.get('flight_pk'))
        if form.is_valid():
            for passenger in passengers:
                age_type = calculate_age(passenger, flight)
                Ticket.objects.create(seat_type=form.cleaned_data['seat_type'],
                                      luggage=form.cleaned_data['luggage'],
                                      passenger=passenger,
                                      customer=request.user,
                                      flight=flight,
                                      age_type=age_type
                                      )
            request.session['report'] = create_bill_ticket(passengers, request.user.email, flight)
            return redirect('report')
        context = {'form': form}
        return render(request, self.template_name, context)


class BookPassengerView(CreateView):

    def get(self, request):
        form = PassengerForm()
        passenger_form_set = formset_factory(PassengerForm, extra=request.session.get('quantity_passenger'))
        formset = passenger_form_set
        flight = Flight.objects.get(pk=request.session.get('flight_pk'))
        return render(request, 'book_passenger.html', {'flight': flight, 'form': formset})

    def post(self, request, *args, **kwargs):
        request.session['booked_passengers'] = []
        passenger_form_set = formset_factory(PassengerForm, extra=request.session.get('quantity_passenger'))
        formset = passenger_form_set(request.POST)
        for form in formset:
            form.empty_permitted = False
            if form.is_valid():
                passenger = Passenger.objects.create(**form.cleaned_data)
                request.session['booked_passengers'].append(passenger.pk)
            else:
                flight = Flight.objects.get(pk=request.session.get('flight_pk'))
                return render(request, 'book_passenger.html', {'flight': flight, 'form': formset})
        return redirect('book_ticket')


class BookView(CreateView):
    form_class = QuantityPassengerForm
    template_name = "book.html"

    def get(self, request, pk_flight):
        form = QuantityPassengerForm
        flight = Flight.objects.get(pk=pk_flight)
        request.session['flight_pk'] = pk_flight
        return render(request, 'book.html', {'flight': flight, 'form': form})

    def post(self, request, *args, **kwargs):
        form = QuantityPassengerForm(request.POST)
        if form.is_valid():
            request.session['quantity_passenger'] = form.cleaned_data['quantity_passenger']
            return redirect('book_passenger')
        context = {'form': form}
        return render(request, self.template_name, context)


class ReportView(View):
    def get(self, request):
        report = request.session.get('report')
        template = 'report.html'
        return render(request, template, {'report': report})
