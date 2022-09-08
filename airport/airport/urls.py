from django.contrib import admin
from django.urls import path, include

from customer.views import HomeView, FlightView, BookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customer.urls')),
    path('', HomeView.as_view(), name='home'),
    path('flight/', FlightView.as_view(), name='flight'),
    path('book/<int:pk>/', BookView.as_view(), name='book'),
]
