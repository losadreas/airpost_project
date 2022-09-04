from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

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
    success_url = reverse_lazy("confirm_email")
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(email=request.POST.get("email"))
            account_activation_token = PasswordResetTokenGenerator()
            user.token = account_activation_token.make_token(user)
            user.is_active = False
            user.save()
            message = f'Verify email Follow the link {request._current_scheme_host}/users/verify_email/{user.token}/{str(urlsafe_base64_encode(force_bytes(user.pk)))}/'
            email = EmailMessage('Verify email', message, from_email=DEFAULT_FROM_EMAIL, to=[user.email])
            email.send()
            return redirect('confirm_email')
        context = {'form': form}
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        logout(request)
        result = super(SignUp, self).get(request, *args, **kwargs)
        return result