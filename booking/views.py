from django.shortcuts import render, redirect, get_object_or_404
from .models import Flight, Booking
from django.urls import reverse
from django.http import HttpResponseRedirect

# Full list of all airport codes and names
AIRPORT_LIST = [
    ("NZNE", "Dairy Flat"),
    ("YMML", "Melbourne"),
    ("NZRO", "Rotorua"),
    ("NZGB", "Claris (Great Barrier Island)"),
    ("NZCI", "Tuuta (Chatham Islands)"),
    ("NZTL", "Lake Tekapo"),
]

# Dictionary version for name lookup
airport_names = dict(AIRPORT_LIST)

# Landing page with search and results
def landing_page(request):
    context = {
        'airports': AIRPORT_LIST,
        'airport_names': airport_names
    }

    from_airport = request.GET.get('from_airport')
    to_airport = request.GET.get('to_airport')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if from_airport and to_airport and start_date and end_date:
        flights = Flight.objects.filter(
            from_airport__icontains=from_airport,
            to_airport__icontains=to_airport,
            date__gte=start_date,
            date__lte=end_date
        )
        context['flights'] = flights

    return render(request, 'index.html', context)

# Book a flight and show confirmation using PRG pattern
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    error = None
    booking = None

    if request.method == 'POST':
        if flight.seats_available <= 0:
            error = 'Sorry, this flight is fully booked.'
        else:
            passenger_name = request.POST.get('passenger_name')
            email = request.POST.get('email')

            if passenger_name and email:
                booking = Booking.objects.create(
                    passenger_name=passenger_name,
                    email=email,
                    flight=flight
                )
                flight.seats_available -= 1
                flight.save()

                return redirect(f"{reverse('book_flight', args=[flight.id])}?confirmed=1&booking_id={booking.id}")
            else:
                error = 'Please enter your name and email.'

    booking_confirmed = request.GET.get('confirmed') == '1'
    booking_id = request.GET.get('booking_id')

    if booking_confirmed and booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, 'book_flight.html', {
        'flight': flight,
        'airport_names': airport_names,
        'booking_confirmed': booking_confirmed,
        'booking': booking,
        'booking_reference': booking.booking_ref if booking else None,
        'error': error
    })

def booking_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    flight = booking.flight

    return render(request, 'invoice.html', {
        'booking': booking,
        'flight': flight,
        'airport_names': airport_names,
        'passenger_name': booking.passenger_name,
        'email': booking.email,
    })

def view_bookings(request):
    bookings = None
    error = None

    name = request.POST.get('name') or request.GET.get('name', '')
    email = request.POST.get('email') or request.GET.get('email', '')

    if name and email:
        bookings = Booking.objects.filter(passenger_name__iexact=name, email__iexact=email)
        if not bookings.exists():
            error = "No bookings found for that name and email."

    elif request.GET.get('clear') == '1':
        name = ''
        email = ''
        bookings = None

    return render(request, 'my_bookings.html', {
        'bookings': bookings,
        'name': name,
        'email': email,
        'error': error,
        'airport_names': airport_names
    })

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    flight = booking.flight
    booking.delete()

    flight.seats_available += 1
    flight.save()

    name = request.POST.get('name', '')
    email = request.POST.get('email', '')

    redirect_url = f"{reverse('view_bookings')}?name={name}&email={email}"
    return HttpResponseRedirect(redirect_url)