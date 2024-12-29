from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Room, Booking, Amenity
from .forms import BookingForm, BookingEditForm, CustomUserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction

def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect("home")
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    login(request, user)
                    messages.success(request, "Registration successful! Welcome to our hotel.")
                    return redirect("home")
            except Exception as e:
                messages.error(request, f"An error occurred during registration. Please try again.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def home(request):
    featured_rooms = Room.objects.filter(available=True)[:3]  # Add featured rooms
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'DEFAULT_FILE_STORAGE': settings.DEFAULT_FILE_STORAGE,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
        'featured_rooms': featured_rooms,
    }
    return render(request, 'home.html', context)

def room_list(request):
    rooms = Room.objects.filter(available=True)
    amenities = Amenity.objects.all()  # Add amenities for filtering
    
    # Filter handling
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')
    selected_amenities = request.GET.getlist('amenities')
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if selected_amenities:
        rooms = rooms.filter(amenities__id__in=selected_amenities).distinct()

    context = {
        'rooms': rooms,
        'amenities': amenities,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'selected_room_type': room_type,
        'selected_max_price': max_price,
        'selected_amenities': selected_amenities,
    }
    return render(request, 'select_room.html', context)

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if not room.available:
        messages.error(request, "This room is currently not available for booking.")
        return redirect('room_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    booking = form.save(commit=False)
                    booking.room = room
                    booking.user = request.user
                    booking.total_price = room.price * (booking.check_out_date - booking.check_in_date).days
                    booking.status = 'CONFIRMED'
                    
                    # Check room availability
                    if not is_room_available(room, booking.check_in_date, booking.check_out_date, None):
                        raise ValidationError("The room is not available for the selected dates")
                    
                    booking.save()
                    
                    # Send confirmation email
                    try:
                        send_booking_confirmation_email(booking)
                    except Exception as e:
                        messages.warning(request, "Booking confirmed, but we couldn't send the confirmation email.")
                    
                    messages.success(request, 'Your booking has been confirmed successfully!')
                    return redirect(reverse('booking_confirmation', args=[booking.id]))
                    
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "An error occurred while processing your booking. Please try again.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        initial_data = {
            'guest_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        }
        form = BookingForm(initial=initial_data)
    
    context = {
        'room': room,
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'book.html', context)

@login_required
def user_bookings(request):
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__gte=timezone.now().date()
    ).order_by('check_in_date')
    
    past_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__lt=timezone.now().date()
    ).order_by('-check_in_date')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    }
    return render(request, 'user_bookings.html', context)

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user owns this booking
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this booking.")
    
    # Check if booking is in the past
    if booking.check_in_date < timezone.now().date():
        messages.error(request, "Cannot edit past bookings.")
        return redirect('user_bookings')
    
    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                with transaction.atomic():
                    if not is_room_available(booking.room, 
                                          form.cleaned_data['check_in_date'],
                                          form.cleaned_data['check_out_date'],
                                          booking.id):
                        raise ValidationError("The room is not available for the selected dates")
                    
                    booking = form.save(commit=False)
                    booking.total_price = booking.room.price * (booking.check_out_date - booking.check_in_date).days
                    booking.save()
                    
                    messages.success(request, 'Your booking has been successfully updated.')
                    return redirect('user_bookings')
                    
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "An error occurred while updating your booking.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = BookingEditForm(instance=booking)
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Check cancellation policy
            check_in_datetime = timezone.make_aware(
                datetime.combine(booking.check_in_date, datetime.min.time())
            )
            
            if check_in_datetime <= timezone.now():
                messages.error(request, 'Cannot cancel a booking that has already started.')
            elif check_in_datetime <= timezone.now() + timedelta(days=1):
                messages.error(request, 'Bookings can only be cancelled more than 24 hours before check-in.')
            else:
                booking.delete()
                messages.success(request, 'Your booking has been successfully cancelled.')
                
                # Send cancellation email
                try:
                    send_cancellation_email(booking)
                except Exception:
                    messages.warning(request, "Booking cancelled, but we couldn't send the cancellation email.")
                    
        except Exception as e:
            messages.error(request, "An error occurred while cancelling your booking.")
            
    return redirect('user_bookings')

# Helper Functions
def is_room_available(room, check_in_date, check_out_date, exclude_booking_id=None):
    """Check if a room is available for the given dates."""
    overlapping_bookings = Booking.objects.filter(
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    )
    
    if exclude_booking_id:
        overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking_id)
        
    return not overlapping_bookings.exists()

def send_booking_confirmation_email(booking):
    """Send booking confirmation email."""
    subject = 'Booking Confirmation'
    message = f'''
    Dear {booking.guest_name},
    
    Your booking at {booking.room.name} has been confirmed!
    
    Booking Details:
    Check-in: {booking.check_in_date}
    Check-out: {booking.check_out_date}
    Total Price: ${booking.total_price}
    
    Thank you for choosing our hotel!
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        fail_silently=False,
    )

def send_cancellation_email(booking):
    """Send booking cancellation email."""
    subject = 'Booking Cancellation Confirmation'
    message = f'''
    Dear {booking.guest_name},
    
    Your booking at {booking.room.name} has been cancelled.
    
    Booking Details:
    Check-in: {booking.check_in_date}
    Check-out: {booking.check_out_date}
    
    We hope to see you another time!
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        fail_silently=False,
    )
