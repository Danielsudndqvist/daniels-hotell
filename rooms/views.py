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
    featured_rooms = Room.objects.filter(available=True)[:3]
    context = {
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
        'featured_rooms': featured_rooms,
    }
    return render(request, 'home.html', context)


def room_list(request):
    """Display list of available rooms with filtering options."""
    rooms = Room.objects.filter(available=True)

    # Filter handling
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')

    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    context = {
        'rooms': rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
        'selected_room_type': room_type,
        'selected_max_price': max_price,
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
            'email': request.user.email
        }
        form = BookingForm(initial=initial_data)

    context = {
        'room': room,
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'book.html', context)


def booking_confirmation(request, booking_id):
    """Show booking confirmation page."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(
        request,
        'booking_confirmation.html',
        {'booking': booking}
    )


def check_availability(request):
    """Check room availability for given dates."""
    if request.method == 'GET':
        check_in = parse_date(request.GET.get('check_in'))
        check_out = parse_date(request.GET.get('check_out'))

        if check_in and check_out:
            available_rooms = Room.objects.filter(
                available=True
            ).exclude(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in
            )
            context = {
                'rooms': available_rooms,
                'check_in': check_in,
                'check_out': check_out
            }
            return render(request, 'available_rooms.html', context)

    return redirect('room_list')


def room_details(request, room_id):
    """Get detailed information about a specific room."""
    room = get_object_or_404(Room, id=room_id)
    data = {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "room_type": room.get_room_type_display(),
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

    context = {
        'rooms': rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'search_results.html', context)


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'home')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')


@login_required
def user_bookings(request):
    """Display user's bookings."""
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__gte=timezone.now().date()
    ).order_by('check_in_date')
    
    past_bookings = Booking.objects.filter(
        user=request.user,
        check_in_date__lt=timezone.now().date()
    ).order_by('-check_in_date')
    
    print(f"Upcoming bookings: {upcoming_bookings.count()}")
    print(f"Past bookings: {past_bookings.count()}")
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    }
    return render(request, 'user_bookings.html', context)


@login_required
def edit_booking(request, booking_id):
    """Handle editing of existing bookings."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.check_in_date < timezone.now().date():
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

    return render(
        request,
        'edit_booking.html',
        {'form': form, 'booking': booking}
    )


@login_required
def cancel_booking(request, booking_id):
    """Handle booking cancellation."""
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"Username: {request.user.username}")
    print(f"Booking ID: {booking_id}")

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    print(f"Found booking: {booking}")

    if request.method == 'POST':
        try:
            # Get current time and ensure it's timezone-aware
            current_time = timezone.now()  # This is already timezone-aware
            print(f"Current time: {current_time}")
            print(f"Current time tzinfo: {current_time.tzinfo}")

            # Convert check-in date to timezone-aware datetime
            check_in_datetime = timezone.make_aware(
                datetime.combine(booking.check_in_date, datetime.min.time())
            )

            # Convert both to UTC for comparison
            current_time_utc = current_time.astimezone(timezone.utc)
            check_in_utc = check_in_datetime.astimezone(timezone.utc)

            print(f"Current time UTC: {current_time_utc}")
            print(f"Check-in time UTC: {check_in_utc}")

            if check_in_utc <= current_time_utc:
                print("Cannot cancel: Booking has already started")
                messages.error(
                    request,
                    'Cannot cancel a booking that has already started.'
                )
            elif check_in_utc <= current_time_utc + timedelta(days=1):
                print("Cannot cancel: Less than 24 hours before check-in")
                messages.error(
                    request,
                    'Bookings must be cancelled more than 24 hours before.'
                )
            else:
                print("Proceeding with cancellation")
                booking.delete()
                print("Booking deleted successfully")
                messages.success(
                    request,
                    'Your booking has been successfully cancelled.'
                )
                return redirect('user_bookings')

        except Exception as e:
            print(f"Error during cancellation: {str(e)}")
            print(f"Error type: {type(e)}")
            messages.error(
                request,
                'An error occurred while cancelling your booking.'
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
    """Send confirmation email for cancelled bookings."""
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
