from django.contrib import admin
from leros.models import *
# Register your models here.

admin.site.register(Sport)
admin.site.register(Activity)
admin.site.register(Facility)
admin.site.register(Status)
admin.site.register(Condition)
admin.site.register(Sex)
admin.site.register(Place)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('status', 'time', 'place')
	ordering = ('-time',)
admin.site.register(Booking, BookingAdmin)