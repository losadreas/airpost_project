from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from airport.settings import DEFAULT_FROM_EMAIL
from customer.forms import CustomUserCreationForm
from django.core.mail import EmailMessage

Customer = get_user_model()


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
    #success_url = reverse_lazy("confirm_email")
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
            message = f'Verify email Follow the link {request._current_scheme_host}/users/verify_email/{user.token}/{str(urlsafe_base64_encode(force_bytes(customer.pk)))}/'
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
        return redirect('addition_info')