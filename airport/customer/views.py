from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from airport.settings import DEFAULT_FROM_EMAIL
from customer.forms import *
from django.core.mail import EmailMessage
from customer.models import Ticket, Passenger, Flight

Customer = get_user_model()


class HomeView(View):
    def get(self, request):
        template = "home.html"
        return render(request, template)


class ConfirmEmail(View):
    def get(self, request, *args, **kwargs):
        template = "confirm_email.html"
        return render(request, template)


class CheckLink(View):
    def get(self, request, *args, **kwargs):
        template = "check_link.html"
        return render(request, template)


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy("confirm_email")
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
            message = f'Verify email Follow the link {request._current_scheme_host}/customers/verify_email/{customer.token}/{str(urlsafe_base64_encode(force_bytes(customer.pk)))}/'
            email = EmailMessage('Verify email', message, from_email=DEFAULT_FROM_EMAIL, to=[customer.email])
            email.send()
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

    def get(self, request, pk_flight, pk_passenger):
        form = TicketForm()
        passenger = Passenger.objects.get(pk=pk_passenger)
        flight = Flight.objects.get(pk=pk_flight)
        return render(request, 'book_ticket.html', {'flight': flight, 'form': form, 'passenger': passenger})

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST, instance=request.user)
        if form.is_valid():
            Ticket.objects.create(seat_type=form.cleaned_data['seat_type'],
                                  luggage=form.cleaned_data['luggage'],
                                  option=form.cleaned_data['option'],
                                  passenger=Passenger.objects.get(pk=kwargs['pk_passenger']),
                                  customer=request.user,
                                  flight=Flight.objects.get(pk=kwargs['pk_flight'])
                                  )
            return redirect('customer_cabinet')
        context = {'form': form}
        return render(request, self.template_name, context)


class BookPassengerView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = "book_passenger.html"

    def get(self, request, pk):
        form = PassengerForm()
        flight = Flight.objects.get(pk=pk)
        return render(request, 'book_passenger.html', {'flight': flight, 'form': form})

    def post(self, request, *args, **kwargs):
        form = PassengerForm(request.POST, instance=request.user)
        if form.is_valid():
            passenger = Passenger.objects.create(first_name=form.cleaned_data['first_name'],
                                                 last_name=form.cleaned_data['last_name'],
                                                 passport=form.cleaned_data['passport'],
                                                 sex=form.cleaned_data['sex'])
            return redirect('book_ticket', pk_passenger=passenger.pk, pk_flight=kwargs['pk'])
        context = {'form': form}
        return render(request, self.template_name, context)
