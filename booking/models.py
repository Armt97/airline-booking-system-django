from django.db import models
import random
import string
from datetime import datetime, timedelta
import pytz

# Define timezones
TIMEZONE_CHOICES = [
    ('Pacific/Auckland', 'Mainland NZ'),
    ('Pacific/Chatham', 'Chatham Islands'),
    ('Australia/Melbourne', 'Melbourne'),
]

class Aircraft(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    from_airport = models.CharField(max_length=10)
    to_airport = models.CharField(max_length=10)
    date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.DurationField(null=True, blank=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    seats_available = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    # Timezone fields
    origin_timezone = models.CharField(max_length=30, choices=TIMEZONE_CHOICES, default='Pacific/Auckland')
    destination_timezone = models.CharField(max_length=30, choices=TIMEZONE_CHOICES, default='Pacific/Auckland')

    def save(self, *args, **kwargs):
        airport_timezone_map = {
            'NZNE': 'Pacific/Auckland',
            'NZRO': 'Pacific/Auckland',
            'NZGB': 'Pacific/Auckland',
            'NZTL': 'Pacific/Auckland',
            'NZCI': 'Pacific/Chatham',
            'YMML': 'Australia/Melbourne',
        }

        self.origin_timezone = airport_timezone_map.get(self.from_airport, 'Pacific/Auckland')
        self.destination_timezone = airport_timezone_map.get(self.to_airport, 'Pacific/Auckland')

        super().save(*args, **kwargs)

    def get_duration(self):
        origin_tz = pytz.timezone(self.origin_timezone)
        destination_tz = pytz.timezone(self.destination_timezone)

        # Localized datetimes
        dep_naive = datetime.combine(self.date, self.departure_time)
        arr_naive = datetime.combine(self.date, self.arrival_time)

        dep_local = origin_tz.localize(dep_naive)
        arr_local = destination_tz.localize(arr_naive)

        # Convert arrival to origin timezone so we can calculate actual duration
        arr_converted = arr_local.astimezone(origin_tz)

        # Handle next-day arrival
        if arr_converted < dep_local:
            arr_converted += timedelta(days=1)

        duration = arr_converted - dep_local
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"

    @property
    def is_international(self):
        return self.origin_timezone != self.destination_timezone

    def __str__(self):
        return f"{self.flight_number}: {self.from_airport} → {self.to_airport} on {self.date}"

class Booking(models.Model):
    passenger_name = models.CharField(max_length=100)
    email = models.EmailField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_ref = models.CharField(max_length=6, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            while True:
                ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Booking.objects.filter(booking_ref=ref).exists():
                    self.booking_ref = ref
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passenger_name} - {self.flight.flight_number} ({self.booking_ref})"
