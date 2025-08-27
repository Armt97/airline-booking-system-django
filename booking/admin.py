from django.contrib import admin
from .models import Aircraft, Flight, Booking

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'from_airport', 'to_airport', 'date', 'departure_time', 'aircraft', 'seats_available')
    list_filter = ('aircraft', 'from_airport', 'to_airport', 'date')
    search_fields = ('flight_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'email', 'flight', 'booking_ref')
    search_fields = ('passenger_name', 'email', 'booking_ref')
