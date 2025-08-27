from django.core.management.base import BaseCommand
from booking.models import Flight
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Generate future flights for 100 days based on existing base flights"

    def handle(self, *args, **kwargs):
        NUM_DAYS = 100
        today = date.today()
        base_flights = Flight.objects.filter(date__gte=today, date__lte=today + timedelta(days=6))
        created = 0

        for base_flight in base_flights:
            for offset in range(1, NUM_DAYS):  # Skip offset=0 to avoid duplicating base
                new_date = base_flight.date + timedelta(days=offset * 7)

                if new_date > today + timedelta(days=NUM_DAYS):
                    break

                if not Flight.objects.filter(
                    from_airport=base_flight.from_airport,
                    to_airport=base_flight.to_airport,
                    date=new_date,
                    departure_time=base_flight.departure_time
                ).exists():
                    Flight.objects.create(
                        from_airport=base_flight.from_airport,
                        to_airport=base_flight.to_airport,
                        date=new_date,
                        departure_time=base_flight.departure_time,
                        arrival_time=base_flight.arrival_time,
                        origin_timezone=base_flight.origin_timezone,
                        destination_timezone=base_flight.destination_timezone,
                        seats_available=base_flight.seats_available,
                        aircraft=base_flight.aircraft,
                        price=base_flight.price,
                        flight_number=f"{base_flight.flight_number}_{new_date.strftime('%Y%m%d')}"
                    )
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} future flights created."))
