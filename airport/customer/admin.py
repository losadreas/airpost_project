from django.contrib import admin
from customer.models import *

admin.site.register(Customer)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Flight)