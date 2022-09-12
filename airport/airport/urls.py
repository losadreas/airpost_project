from django.contrib import admin
from django.urls import path, include

from customer.views import HomeView, FlightView, BookTicketView, BookPassengerView, BookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customer.urls')),
    path('', HomeView.as_view(), name='home'),
    path('flight/', FlightView.as_view(), name='flight'),
    path('book/<int:pk_flight>/', BookView.as_view(), name='book'),
    path('book_passenger/', BookPassengerView.as_view(), name='book_passenger'),
    path('book_ticket/', BookTicketView.as_view(), name='book_ticket'),
    path('staff/', include('staff.urls'))
]
