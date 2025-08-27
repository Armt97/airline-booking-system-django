from django.core.management.base import BaseCommand
from booking.models import Flight
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Update flight durations based on departure and arrival times'

    def handle(self, *args, **kwargs):
        updated = 0
        for flight in Flight.objects.all():
            if flight.departure_time and flight.arrival_time:
                # convert times to datetime to subtract
                today = datetime.today().date()
                dep = datetime.combine(today, flight.departure_time)
                arr = datetime.combine(today, flight.arrival_time)

                # Handle overnight flights
                if arr < dep:
                    arr += timedelta(days=1)

                flight.duration = arr - dep
                flight.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Updated durations for {updated} flights."))

