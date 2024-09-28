from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import JsonResponse
from .models import Room, Booking, Amenity
from .forms import BookingForm
from django.core.mail import send_mail
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def room_list(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'select_room.html', {'rooms': rooms})

def select_room(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'select_room.html', {'rooms': rooms})

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.total_price = room.price * (booking.check_out_date - booking.check_in_date).days
            booking.status = 'CONFIRMED'

            # Check room availability
            overlapping_bookings = Booking.objects.filter(
                Q(room=room) &
                Q(check_in_date__lt=booking.check_out_date) &
                Q(check_out_date__gt=booking.check_in_date)
            )
            if overlapping_bookings.exists():
                messages.error(request, "The room is not available for the selected dates")
            else:
                try:
                    booking.save()
                    
                    # Send confirmation emails
                    try:
                        send_mail(
                            'Booking Confirmation',
                            f'Thank you for your booking, {booking.guest_name}! Your stay at {room.name} from {booking.check_in_date} to {booking.check_out_date} is confirmed.',
                            'your_email@example.com',
                            [booking.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        messages.warning(request, f"Booking confirmed, but failed to send email: {e}")
                    
                    messages.success(request, 'Booking confirmed successfully!')
                    return redirect(reverse('booking_confirmation', args=[booking.id]))
                except Exception as e:
                    messages.error(request, f"An error occurred while saving the booking: {e}")
        else:
            messages.error(request, f"Form is invalid. Errors: {form.errors}")
    else:
        form = BookingForm()
    
    return render(request, 'book.html', {'room': room, 'form': form})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def check_availability(request):
    if request.method == 'GET':
        check_in = parse_date(request.GET.get('check_in'))
        check_out = parse_date(request.GET.get('check_out'))
        
        if check_in and check_out:
            available_rooms = Room.objects.filter(available=True).exclude(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in
            )
            return render(request, 'available_rooms.html', {'rooms': available_rooms, 'check_in': check_in, 'check_out': check_out})
    
    return redirect('select_room')

def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    data = {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "room_type": room.get_room_type_display(),
        "price": float(room.price),
        "images": [img.image.url for img in room.images.all()],
        "amenities": [amenity.name for amenity in room.amenities.all()],
        "max_occupancy": room.max_occupancy,
        "size": room.size
    }
    
    return JsonResponse(data)

def room_details_json(request, room_id):
    return room_details(request, room_id)

def search_rooms(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')

    rooms = Room.objects.filter(available=True)

    if check_in and check_out:
        check_in = parse_date(check_in)
        check_out = parse_date(check_out)
        rooms = rooms.exclude(
            booking__check_in_date__lt=check_out,
            booking__check_out_date__gt=check_in
        )

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    return render(request, 'search_results.html', {'rooms': rooms})

def amenities_list(request):
    amenities = Amenity.objects.all()
    return render(request, 'amenities_list.html', {'amenities': amenities})

def user_bookings(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(email=request.user.email).order_by('-check_in_date')
        return render(request, 'user_bookings.html', {'bookings': bookings})
    else:
        messages.error(request, "Please log in to view your bookings.")
        return redirect('login')