from django.contrib import admin
from django.urls import path, include

from customer.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customer.urls')),
    path('', HomeView.as_view(), name='home'),
]
