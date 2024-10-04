from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import JsonResponse
from .models import Room, Booking, Amenity
from .forms import BookingForm, BookingEditForm, CustomUserCreationForm
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, "Registration successful.")  # Show success message
            return redirect("home")  # Redirect to the home page
        messages.error(request, "Unsuccessful registration. Invalid information.")  # Show error message if form is invalid
    else:
        form = CustomUserCreationForm()  # Create a new empty form
    return render(request, "register.html", {"form": form})  # Render the registration template with the form

# Home page view
def home(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'DEFAULT_FILE_STORAGE': settings.DEFAULT_FILE_STORAGE,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'home.html', context)  # Render the home page template

# Room listing view for available rooms
def room_list(request):
    rooms = Room.objects.filter(available=True)  # Get all available rooms
    context = {
        'rooms': rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'select_room.html', context)  # Render the room selection template

# Redundant room selection view (similar to room_list)
def select_room(request):
    rooms = Room.objects.filter(available=True)  # Get all available rooms
    context = {
        'rooms': rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'select_room.html', context)  # Render the room selection template

@login_required  # Require user to be logged in
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Get the room by ID or return a 404 error
    
    if request.method == 'POST':
        form = BookingForm(request.POST)  # Initialize booking form with POST data
        if form.is_valid():
            booking = form.save(commit=False)  # Create booking instance but don't save yet
            booking.room = room  # Assign the room to the booking
            booking.user = request.user  # Assign the logged-in user to the booking
            booking.total_price = room.price * (booking.check_out_date - booking.check_in_date).days  # Calculate total price
            booking.status = 'CONFIRMED'  # Set initial status
            
            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                Q(room=room) &
                Q(check_in_date__lt=booking.check_out_date) &
                Q(check_out_date__gt=booking.check_in_date)
            )
            if overlapping_bookings.exists():
                messages.error(request, "The room is not available for the selected dates")  # Show error if room is not available
            else:
                try:
                    booking.save()  # Save the booking
                    
                    # Send confirmation email
                    try:
                        send_mail(
                            'Booking Confirmation',
                            f'Thank you for your booking, {booking.guest_name}! Your stay at {room.name} from {booking.check_in_date} to {booking.check_out_date} is confirmed.',
                            'rkso6qnt@students.codeinstitute.net',  # Replace with your email
                            [booking.email],  # Send to the guest's email
                            fail_silently=False,
                        )
                    except Exception as e:
                        messages.warning(request, f"Booking confirmed, but failed to send email: {e}")  # Warn if email sending fails
                    
                    messages.success(request, 'Booking confirmed successfully!')  # Show success message
                    return redirect(reverse('booking_confirmation', args=[booking.id]))  # Redirect to the booking confirmation page
                except Exception as e:
                    messages.error(request, f"An error occurred while saving the booking: {e}")  # Show error if saving fails
        else:
            messages.error(request, f"Form is invalid. Errors: {form.errors}")  # Show form validation errors
    else:
        form = BookingForm()  # Create a new empty form
    
    context = {
        'room': room,
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'book.html', context)  # Render the booking form template

# Booking confirmation view
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Get booking by ID or return 404
    return render(request, 'booking_confirmation.html', {'booking': booking})  # Render the confirmation template

# Check room availability for selected dates
def check_availability(request):
    if request.method == 'GET':
        check_in = parse_date(request.GET.get('check_in'))  # Parse check-in date
        check_out = parse_date(request.GET.get('check_out'))  # Parse check-out date
        
        if check_in and check_out:
            # Get available rooms excluding those booked during the specified dates
            available_rooms = Room.objects.filter(available=True).exclude(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in
            )
            return render(request, 'available_rooms.html', {'rooms': available_rooms, 'check_in': check_in, 'check_out': check_out})  # Render available rooms template
    
    return redirect('select_room')  # Redirect if no valid dates provided

# View for retrieving room details
def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Get room by ID or return 404
    
    data = {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "room_type": room.get_room_type_display(),  # Get human-readable room type
        "price": float(room.price),  # Room price
        "images": [img.image.url for img in room.images.all()],  # List of image URLs
        "amenities": [amenity.name for amenity in room.amenities.all()],  # List of amenity names
        "max_occupancy": room.max_occupancy,  # Maximum occupancy
        "size": room.size  # Size of the room
    }
    
    return JsonResponse(data)  # Return room details as JSON response

# Redirect to room details view for JSON response (same logic as room_details)
def room_details_json(request, room_id):
    return room_details(request, room_id)  # Use room_details function to handle logic

# Search rooms based on criteria
def search_rooms(request):
    check_in = request.GET.get('check_in')  # Get check-in date
    check_out = request.GET.get('check_out')  # Get check-out date
    room_type = request.GET.get('room_type')  # Get room type
    max_price = request.GET.get('max_price')  # Get maximum price

    rooms = Room.objects.filter(available=True)  # Start with all available rooms

    # Filter rooms based on check-in and check-out dates
    if check_in and check_out:
        check_in = parse_date(check_in)
        check_out = parse_date(check_out)
        rooms = rooms.exclude(
            booking__check_in_date__lt=check_out,
            booking__check_out_date__gt=check_in
        )

    # Filter by room type if provided
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    # Filter by maximum price if provided
    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    context = {
        'rooms': rooms,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'storage_backend': default_storage.__class__.__name__,
        'GS_BUCKET_NAME': getattr(settings, 'GS_BUCKET_NAME', 'Not Set'),
    }
    return render(request, 'search_results.html', context)  # Render search results template

# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # Get username from POST data
        password = request.POST['password']  # Get password from POST data
        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log the user in
            next_url = request.POST.get('next', 'home')  # Get next URL to redirect to
            return redirect(next_url)  # Redirect to the next URL
        else:
            messages.error(request, 'Invalid username or password')  # Show error if authentication fails
    return render(request, 'login.html')  # Render login template

# User logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the home page

@login_required  # Require user to be logged in
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-check_in_date')  # Get bookings for the logged-in user
    return render(request, 'user_bookings.html', {'bookings': bookings})  # Render user's bookings template

@login_required  # Require user to be logged in
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Get booking by ID or return 404
    
    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)  # Initialize edit form with booking instance
        if form.is_valid():
            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                Q(room=booking.room) &
                Q(check_in_date__lt=form.cleaned_data['check_out_date']) &
                Q(check_out_date__gt=form.cleaned_data['check_in_date'])
            ).exclude(id=booking.id)  # Exclude the current booking
            
            if overlapping_bookings.exists():
                messages.error(request, "The room is not available for the selected dates")  # Show error if room is not available
            else:
                booking = form.save(commit=False)  # Save changes to booking but don't commit yet
                booking.total_price = booking.room.price * (booking.check_out_date - booking.check_in_date).days  # Recalculate total price
                booking.save()  # Save the booking
                messages.success(request, 'Your booking has been successfully updated.')  # Show success message
                return redirect('user_bookings')  # Redirect to user's bookings
    else:
        form = BookingEditForm(instance=booking)  # Create a new form instance with existing booking data
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})  # Render the edit booking template


@login_required  # Require user to be logged in
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Get booking by ID or return 404
    if request.method == 'POST':
        # Convert booking check_in_date to datetime if necessary
        if isinstance(booking.check_in_date, timezone.datetime):
            check_in_date = booking.check_in_date  # Already a datetime
        else:
            check_in_date = timezone.make_aware(datetime.combine(booking.check_in_date, datetime.min.time()))  # Combine date with time

        # Check if the cancellation is more than 24 hours before check-in
        if check_in_date > timezone.now() + timezone.timedelta(days=1):
            booking.delete()  # Delete the booking
            messages.success(request, 'Your booking has been successfully cancelled.')  # Show success message
        else:
            messages.error(request, 'Bookings can only be cancelled more than 24 hours before check-in.')  # Show error if cancellation is too late
    return redirect('user_bookings')  # Redirect to user's bookings