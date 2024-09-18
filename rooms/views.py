from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Room, Booking
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def base_page(request):
    return render(request, 'base.html')

def room_list(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'list.html', {'rooms': rooms})

def select_room(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'select_room.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        try:
            # Extract data from the form
            guest_name = request.POST['guest_name']
            email = request.POST['email']
            phone = request.POST['phone']
            check_in_date = parse_date(request.POST['check_in_date'])
            check_out_date = parse_date(request.POST['check_out_date'])

            # Validate dates
            if check_in_date >= check_out_date:
                raise ValueError("Check-in date must be before check-out date")

            # Calculate total price based on room price and duration of stay
            total_price = room.price * (check_out_date - check_in_date).days

            # Create and save the booking
            booking = Booking.objects.create(
                guest_name=guest_name,
                email=email,
                phone=phone,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                room=room,
                total_price=total_price,
                status='confirmed'
            )

            # Send confirmation emails to both admin and guest
            send_mail(
                'New Booking Confirmation',
                f'A new booking has been made for {booking.guest_name} in {room.name}. Check-in date: {check_in_date}, Check-out date: {check_out_date}',
                'admin@example.com',  # Replace with your admin email
                ['admin@example.com'],  # Replace with your admin email
                fail_silently=False,
            )
            send_mail(
                'Booking Confirmation',
                f'Thank you for your booking, {guest_name}! Your stay at {room.name} from {check_in_date} to {check_out_date} is confirmed.',
                'your_email@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            # Redirect to the booking confirmation page
            return redirect(reverse('booking_confirmation', args=[booking.id]))
        except Exception as e:
            print(f"Error creating booking: {str(e)}")
            return render(request, 'book.html', {'room': room, 'error': str(e)})
    else:
        return render(request, 'book.html', {'room': room})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {
        'guest_name': booking.guest_name,
        'email': booking.email,
        'phone': booking.phone,
        'check_in_date': booking.check_in_date,
        'check_out_date': booking.check_out_date,
        'room': booking.room,
        'total_price': booking.total_price,
    })