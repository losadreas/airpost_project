from django.urls import path, include
from customer.views import *

urlpatterns = [
  #  path('logout/', LogOut.as_view(), name='logout'),
  #  path('<int:user_id>/', UserView.as_view(), name='user_view'),
    path('', include('django.contrib.auth.urls')),
    path('register/', SignUp.as_view(), name='register'),
    path('confirm_email/', ConfirmEmail.as_view(), name='confirm_email'),
 #   path('addition_info/', AdditionInfo.as_view(), name='addition_info'),
    path('verify_email/<token>/<pk_code>/', VerifyEmail.as_view(), name="verify_email"),
    path('check_link/', CheckLink.as_view(), name='check_link'),
    ]
