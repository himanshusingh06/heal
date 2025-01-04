from django.contrib import admin
from .models import Service
from .models import Booking
from .models import Event

admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Event)