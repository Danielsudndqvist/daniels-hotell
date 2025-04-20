from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q, Max
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.urls import reverse
from .models import Room, Booking
from .forms import (
    BookingForm,
    BookingEditForm,
    CustomUserCreationForm,
)
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from .utils import log_storage_diagnostics

def register(request):
    """Handle user registration."""
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
                    messages.success(
                        request,
                        "Registration successful! Welcome to our hotel."
                    )
                    return redirect("home")
            except Exception:
                messages.error(
                    request,
                    "An error occurred during registration. Please try again."
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{field.replace('_', ' ').title()}: {error}"
                    )
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def home(request):
    """Render home page with featured rooms."""
    # Get today and tomorrow dates for search form
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Get featured rooms
    featured_rooms = Room.objects.filter(available=True)[:3]
    
    # Use Room.ROOM_TYPES which is defined in your model
    room_types = Room.ROOM_TYPES
    
    context = {
        'today': today,
        'tomorrow': tomorrow,
        'room_types': room_types,
        'featured_rooms': featured_rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'DEFAULT_FILE_STORAGE': settings.DEFAULT_FILE_STORAGE,
        'storage_backend': (
            default_storage.__class__.__name__
        ),
        'GS_BUCKET_NAME': getattr(
            settings,
            'GS_BUCKET_NAME',
            'Not Set'
        ),
    }
    return render(request, 'home.html', context)


def room_list(request):
    """Display list of available rooms with filtering options."""
    # Get all available rooms
    rooms = Room.objects.filter(available=True)

    # Use Room.ROOM_TYPES from your model
    room_types = Room.ROOM_TYPES
    
    # Get today and tomorrow dates for date inputs
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    # Filter handling
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    # Apply filters
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if check_in and check_out:
        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)
        if check_in_date and check_out_date:
            rooms = rooms.exclude(
                booking__check_in_date__lt=check_out_date,
                booking__check_out_date__gt=check_in_date
            )

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'today': today,
        'tomorrow': tomorrow,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
        'selected_room_type': room_type,
        'selected_max_price': max_price,
        'selected_check_in': check_in,
        'selected_check_out': check_out,
    }
    return render(request, 'select_room.html', context)


def room_detail(request, room_id):
    """Display detailed information about a specific room."""
    room = get_object_or_404(Room, id=room_id)
    
    # Get similar rooms (same type or price range)
    similar_rooms = Room.objects.filter(
        Q(room_type=room.room_type) | 
        Q(price__range=(room.price*0.8, room.price*1.2))
    ).exclude(id=room.id)[:3]
    
    # Get today and tomorrow dates for booking form
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    context = {
        'room': room,
        'similar_rooms': similar_rooms,
        'today': today,
        'tomorrow': tomorrow,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    }
    return render(request, 'room_detail.html', context)


@login_required
def book_room(request, room_id):
    """Handle room booking."""
    room = get_object_or_404(Room, id=room_id)
    
    # Get today and tomorrow dates for form
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if not room.available:
        messages.error(request, "This room is currently not available for booking.")
        return redirect('room_list')

    # Get check-in and check-out dates from query params if available
    initial_check_in = request.GET.get('check_in')
    initial_check_out = request.GET.get('check_out')
    
    if initial_check_in:
        try:
            initial_check_in = parse_date(initial_check_in)
        except:
            initial_check_in = None
    
    if initial_check_out:
        try:
            initial_check_out = parse_date(initial_check_out)
        except:
            initial_check_out = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    booking = form.save(commit=False)
                    booking.room = room
                    booking.user = request.user
                    days = (booking.check_out_date - booking.check_in_date).days
                    booking.total_price = room.price * days
                    booking.status = 'CONFIRMED'

                    if not is_room_available(room, booking.check_in_date, booking.check_out_date, None):
                        raise ValidationError("Room not available for selected dates")

                    booking.full_clean()  # This will validate the model
                    booking.save()
                    send_booking_confirmation_email(booking)
                    messages.success(request, 'Booking confirmed successfully!')
                    return redirect(reverse('booking_confirmation', args=[booking.id]))
            except ValidationError as e:
                # Add form errors for any validation errors
                for field, error in e.message_dict.items():
                    form.add_error(field, error)
        
        # If the form is not valid or there were validation errors, display them
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        initial_data = {
            'guest_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'check_in_date': initial_check_in,
            'check_out_date': initial_check_out,
        }
        form = BookingForm(initial=initial_data)

    context = {
        'room': room,
        'form': form,
        'today': today,
        'tomorrow': tomorrow,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'book.html', context)


def booking_confirmation(request, booking_id):
    """Show booking confirmation page."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Get today's date for countdown calculation
    today = datetime.now().date()
    
    context = {
        'booking': booking,
        'today': today,
    }
    return render(request, 'booking_confirmation.html', context)


def check_availability(request):
    """Check room availability for given dates."""
    if request.method == 'GET':
        check_in = parse_date(request.GET.get('check_in'))
        check_out = parse_date(request.GET.get('check_out'))
        
        # Use Room.ROOM_TYPES from your model
        room_types = Room.ROOM_TYPES
        
        # Get today and tomorrow dates for form
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        if check_in and check_out:
            available_rooms = Room.objects.filter(
                available=True
            ).exclude(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in
            )
            context = {
                'rooms': available_rooms,
                'room_types': room_types,
                'today': today,
                'tomorrow': tomorrow,
                'check_in': check_in,
                'check_out': check_out,
                'MEDIA_URL': settings.MEDIA_URL,
                'STATIC_URL': settings.STATIC_URL,
            }
            return render(request, 'available_rooms.html', context)

    return redirect('room_list')


def room_details(request, room_id):
    """Get detailed information about a specific room."""
    room = get_object_or_404(Room, id=room_id)
    
    # Your Room model has get_room_type_display method because room_type uses choices
    data = {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "room_type": room.get_room_type_display(),  # This works because you defined choices
        "price": float(room.price),
        "images": [img.image.url for img in room.images.all()],
        "max_occupancy": room.max_occupancy,
        "size": room.size
    }
    return JsonResponse(data)


def room_details_json(request, room_id):
    """Return room details in JSON format."""
    return room_details(request, room_id)


def search_rooms(request):
    """Search for rooms based on various criteria."""
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')

    # Use Room.ROOM_TYPES from your model
    room_types = Room.ROOM_TYPES
    
    # Get today and tomorrow dates for form
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    rooms = Room.objects.filter(available=True)

    if check_in and check_out:
        check_in_date = parse_date(check_in)
        check_out_date = parse_date(check_out)
        if check_in_date and check_out_date:
            rooms = rooms.exclude(
                booking__check_in_date__lt=check_out_date,
                booking__check_out_date__gt=check_in_date
            )

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'today': today,
        'tomorrow': tomorrow,
        'selected_check_in': check_in,
        'selected_check_out': check_out,
        'selected_room_type': room_type,
        'selected_max_price': max_price,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'search_results.html', context)


def login_view(request):
    """Handle user login."""
    # Add referrer url to context for better redirection
    next_url = request.GET.get('next', '')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'home')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password')
    
    context = {
        'next': next_url
    }
    return render(request, 'login.html', context)


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@login_required
def user_bookings(request):
    """Display user's bookings."""
    # Today's date for determining upcoming vs past bookings
    today = datetime.now().date()
    
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__gte=today
    ).order_by('check_in_date')
    
    past_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__lt=today
    ).order_by('-check_in_date')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'today': today,
    }
    return render(request, 'user_bookings.html', context)


@login_required
def edit_booking(request, booking_id):
    """Handle editing of existing bookings."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Today's date for validation
    today = datetime.now().date()

    if booking.check_in_date < today:
        messages.error(request, "Cannot edit past bookings.")
        return redirect('user_bookings')

    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                with transaction.atomic():
                    if not is_room_available(
                        booking.room,
                        form.cleaned_data['check_in_date'],
                        form.cleaned_data['check_out_date'],
                        booking.id
                    ):
                        raise ValidationError(
                            "Room not available for selected dates"
                        )

                    booking = form.save(commit=False)
                    days = (
                        booking.check_out_date - booking.check_in_date
                    ).days
                    booking.total_price = booking.room.price * days
                    booking.save()

                    messages.success(
                        request,
                        'Your booking has been successfully updated.'
                    )
                    return redirect('user_bookings')
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception:
                messages.error(
                    request,
                    "An error occurred while updating your booking."
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{field.replace('_', ' ').title()}: {error}"
                    )
    else:
        form = BookingEditForm(instance=booking)

    context = {
        'form': form,
        'booking': booking,
        'today': today,
    }
    return render(request, 'edit_booking.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Handle booking cancellation."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        try:
            # Get current time and ensure it's timezone-aware
            current_time = timezone.now()  # This is already timezone-aware

            # Convert check-in date to timezone-aware datetime
            check_in_datetime = timezone.make_aware(
                datetime.combine(booking.check_in_date, datetime.min.time())
            )

            # Convert both to UTC for comparison
            current_time_utc = current_time.astimezone(timezone.utc)
            check_in_utc = check_in_datetime.astimezone(timezone.utc)

            if check_in_utc <= current_time_utc:
                messages.error(
                    request,
                    'Cannot cancel a booking that has already started.'
                )
            elif check_in_utc <= current_time_utc + timedelta(days=1):
                messages.error(
                    request,
                    'Bookings must be cancelled more than 24 hours before check-in.'
                )
            else:
                # Send cancellation email before deleting
                send_cancellation_email(booking)
                booking.delete()
                messages.success(
                    request,
                    'Your booking has been successfully cancelled.'
                )
                return redirect('user_bookings')

        except Exception as e:
            messages.error(
                request,
                f'An error occurred while cancelling your booking: {str(e)}'
            )

    return redirect('user_bookings')


def is_room_available(room, check_in_date, check_out_date, exclude_booking_id):
    """Check if a room is available for given dates."""
    overlapping_bookings = Booking.objects.filter(
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    )

    if exclude_booking_id:
        overlapping_bookings = overlapping_bookings.exclude(
            id=exclude_booking_id
        )

    return not overlapping_bookings.exists()


def send_booking_confirmation_email(booking):
    """Send confirmation email for new bookings."""
    subject = 'Booking Confirmation - Daniel\'s Hotel'
    message = f'''
    Dear {booking.guest_name},

    Your booking at Daniel's Hotel has been confirmed!

    Booking Details:
    Booking Reference: #{booking.id}
    Room: {booking.room.name}
    Check-in: {booking.check_in_date.strftime('%A, %B %d, %Y')} (from 3:00 PM)
    Check-out: {booking.check_out_date.strftime('%A, %B %d, %Y')} (until 11:00 AM)
    Total Price: ${booking.total_price}

    Guest Information:
    Name: {booking.guest_name}
    Email: {booking.email}
    Phone: {booking.phone_number or 'Not provided'}

    If you need to modify or cancel your booking, please log in to your account or contact us.

    Thank you for choosing Daniel's Hotel. We look forward to welcoming you!

    Best regards,
    The Daniel's Hotel Team
    '''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        fail_silently=False,
    )


def send_cancellation_email(booking):
    """Send confirmation email for cancelled bookings."""
    subject = 'Booking Cancellation Confirmation - Daniel\'s Hotel'
    message = f'''
    Dear {booking.guest_name},

    Your booking at Daniel's Hotel has been cancelled successfully.

    Cancelled Booking Details:
    Booking Reference: #{booking.id}
    Room: {booking.room.name}
    Check-in: {booking.check_in_date.strftime('%A, %B %d, %Y')}
    Check-out: {booking.check_out_date.strftime('%A, %B %d, %Y')}

    We hope to have the opportunity to welcome you at Daniel's Hotel in the future.

    If you have any questions, please don't hesitate to contact us.

    Best regards,
    The Daniel's Hotel Team
    '''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email],
        fail_silently=False,
    )
