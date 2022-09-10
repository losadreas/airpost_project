from django.contrib import admin
from django.urls import path, include

from customer.views import HomeView, FlightView, BookTicketView, BookPassengerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customer.urls')),
    path('', HomeView.as_view(), name='home'),
    path('flight/', FlightView.as_view(), name='flight'),
    path('book_passenger/<int:pk>/', BookPassengerView.as_view(), name='book_passenger'),
    path('book_ticket/<int:pk_passenger>/<int:pk_flight>/', BookTicketView.as_view(), name='book_ticket'),
]
