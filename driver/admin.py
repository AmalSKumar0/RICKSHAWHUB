from django.contrib import admin
from .models import Driver,Bookings,CompletedBookings,Reviews,TemporaryDriver

# Register your models here.
admin.site.register(Driver)
admin.site.register(Bookings)
admin.site.register(CompletedBookings)
admin.site.register(Reviews)
admin.site.register(TemporaryDriver)