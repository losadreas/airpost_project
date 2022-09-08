from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from airport.settings import DEFAULT_FROM_EMAIL
from customer.forms import CustomUserCreationForm, TicketForm
from django.core.mail import EmailMessage

from customer.models import Ticket, Passenger, Flight

Customer = get_user_model()


class HomeView(View):
    def get(self, request, *args, **kwargs):
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
        return redirect('customer_cabinet/' + str(customer.pk))


class LogOut(View):
    def get(self, request, *args, **kwargs):
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




class BookView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "book.html"

    def get(self, request, pk):
        form = TicketForm()

        f = Flight.objects.get(pk=pk)
        return render(request, 'book.html', {'flight': f, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST, instance=request.user)
        if form.is_valid():
            Ticket.objects.create(seat_type=form.cleaned_data['seat_type'],
                                  luggage=form.cleaned_data['luggage'],
                                  option=form.cleaned_data['option'],
                                  passenger=form.cleaned_data['passenger'],
                                  customer=request.user,
                                  flight=Flight.objects.get(pk=kwargs['pk'])
                                  )

            return redirect('customer_cabinet')
        context = {'form': form}
        return render(request, self.template_name, context)
