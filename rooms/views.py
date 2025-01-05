from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date

from .forms import (
    BookingEditForm,
    BookingForm,
    CustomUserCreationForm,
)
from .models import Amenity, Booking, Room


def home(request):
    """Render the home page with context."""
    context = {
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "DEFAULT_FILE_STORAGE": settings.DEFAULT_FILE_STORAGE,
        "storage_backend": default_storage.__class__.__name__,
        "GS_BUCKET_NAME": getattr(settings, "GS_BUCKET_NAME", "Not Set"),
    }
    return render(request, "home.html", context)


def room_list(request):
    """Display list of available rooms."""
    rooms = Room.objects.filter(available=True)
    context = {
        "rooms": rooms,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "storage_backend": default_storage.__class__.__name__,
        "GS_BUCKET_NAME": getattr(settings, "GS_BUCKET_NAME", "Not Set"),
    }
    return render(request, "select_room.html", context)


def select_room(request):
    """Handle room selection with filtering options."""
    today = timezone.now().date()
    rooms = Room.objects.filter(available=True)
    room_types = Room.ROOM_TYPES
    amenities = Amenity.objects.all()

    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    room_type = request.GET.get("room_type")
    max_price = request.GET.get("max_price")
    selected_amenities = request.GET.getlist("amenities")

    if check_in and check_out:
        request.session["check_in"] = check_in
        request.session["check_out"] = check_out
        check_in_date = timezone.datetime.strptime(
            check_in, "%Y-%m-%d"
        ).date()
        check_out_date = timezone.datetime.strptime(
            check_out, "%Y-%m-%d"
        ).date()
        rooms = rooms.exclude(
            booking__check_in_date__lt=check_out_date,
            booking__check_out_date__gt=check_in_date,
            booking__status="CONFIRMED",
        )

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    if selected_amenities:
        rooms = rooms.filter(
            amenities__id__in=selected_amenities
        ).distinct()

    context = {
        "rooms": rooms,
        "room_types": room_types,
        "amenities": amenities,
        "today": today,
        "selected_room_type": room_type,
        "selected_amenities": selected_amenities,
    }
    return render(request, "select_room.html", context)


@login_required
def book_room(request, room_id):
    """Handle room booking process."""
    room = get_object_or_404(Room, id=room_id)

    if not room.available:
        messages.error(
            request, "This room is currently not available for booking."
        )
        return redirect("room_list")

    check_in = request.session.get("check_in")
    check_out = request.session.get("check_out")
    if not check_in or not check_out:
        messages.error(
            request, "Please select check-in and check-out dates first."
        )
        return redirect("select_room")

    initial_data = {
        "guest_name": request.user.get_full_name() or request.user.username,
        "email": request.user.email,
        "check_in_date": check_in,
        "check_out_date": check_out,
    }

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.total_price = (
                room.price *
                (booking.check_out_date - booking.check_in_date).days
            )
            booking.status = "CONFIRMED"

            overlapping_bookings = Booking.objects.filter(
                Q(room=room) &
                Q(check_in_date__lt=booking.check_out_date) &
                Q(check_out_date__gt=booking.check_in_date)
            )
            if overlapping_bookings.exists():
                messages.error(
                    request,
                    "The room is not available for the selected dates"
                )
            else:
                try:
                    booking.save()
                    try:
                        email_message = (
                            f"Thank you for your"
                            f"booking,{booking.guest_name}! "
                            f"Your stay at {room.name} from "
                            f"{booking.check_in_date} to "
                            f"{booking.check_out_date} is confirmed."
                        )
                        send_mail(
                            "Booking Confirmation",
                            email_message,
                            "rkso6qnt@students.codeinstitute.net",
                            [booking.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        messages.warning(
                            request,
                            "Booking confirmed, but failed to send email: "
                            f"{str(e)}"
                        )

                    messages.success(request, "Booking confirmed successfully")
                    return redirect(
                        reverse(
                            "booking_confirmation",
                            args=[booking.id]
                        )
                    )
                except Exception as e:
                    messages.error(
                        request,
                        f"An error occurred while saving the booking: {str(e)}"
                    )
        else:
            messages.error(request, f"Form is invalid. Errors: {form.errors}")
    else:
        form = BookingForm(initial=initial_data)

    context = {
        "room": room,
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
    }
    return render(request, "book.html", context)


def booking_confirmation(request, booking_id):
    """Display booking confirmation page."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(
        request, "booking_confirmation.html", {"booking": booking}
    )


def check_availability(request):
    """Check room availability for given dates."""
    if request.method == "GET":
        check_in = parse_date(request.GET.get("check_in"))
        check_out = parse_date(request.GET.get("check_out"))

        if check_in and check_out:
            available_rooms = Room.objects.filter(
                available=True
            ).exclude(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in,
            )
            return render(
                request,
                "available_rooms.html",
                {
                    "rooms": available_rooms,
                    "check_in": check_in,
                    "check_out": check_out,
                },
            )

    return redirect("select_room")


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
        "amenities": [amenity.name for amenity in room.amenities.all()],
        "max_occupancy": room.max_occupancy,
        "size": room.size,
    }
    return JsonResponse(data)


def room_details_json(request, room_id):
    """JSON endpoint for room details."""
    return room_details(request, room_id)


def search_rooms(request):
    """Search rooms based on criteria."""
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    room_type = request.GET.get("room_type")
    max_price = request.GET.get("max_price")

    rooms = Room.objects.filter(available=True)

    if check_in and check_out:
        check_in = parse_date(check_in)
        check_out = parse_date(check_out)
        rooms = rooms.exclude(
            booking__check_in_date__lt=check_out,
            booking__check_out_date__gt=check_in,
        )

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    context = {
        "rooms": rooms,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "storage_backend": default_storage.__class__.__name__,
        "GS_BUCKET_NAME": getattr(settings, "GS_BUCKET_NAME", "Not Set"),
    }
    return render(request, "search_results.html", context)


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "home")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("home")


def register(request):
    """Handle user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information."
        )
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def user_bookings(request):
    """Display user's bookings."""
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-check_in_date")
    return render(request, "user_bookings.html", {"bookings": bookings})


@login_required
def edit_booking(request, booking_id):
    """Handle editing of existing bookings."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = BookingEditForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data["check_in_date"]
            check_out_date = form.cleaned_data["check_out_date"]

            overlapping_bookings = Booking.objects.filter(
                Q(room=booking.room) &
                Q(check_in_date__lt=check_out_date) &
                Q(check_out_date__gt=check_in_date)
            ).exclude(id=booking.id)

            if overlapping_bookings.exists():
                messages.error(
                    request,
                    "The room is not available for the selected dates"
                )
            else:
                booking.check_in_date = check_in_date
                booking.check_out_date = check_out_date
                booking.status = form.cleaned_data["status"]
                booking.total_price = (
                    booking.room.price *
                    (check_out_date - check_in_date).days
                )
                booking.save()
                messages.success(
                    request,
                    "Your booking has been successfully updated."
                )
                return redirect("user_bookings")
    else:
        form = BookingEditForm(instance=booking)

    return render(
        request,
        "edit_booking.html",
        {"form": form, "booking": booking}
    )


@login_required
def cancel_booking(request, booking_id):
    """Handle booking cancellation."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        future_date = timezone.now().date() + timezone.timedelta(days=1)

        if booking.check_in_date > future_date:
            booking.status = "CANCELLED"
            booking.save()
            messages.success(request, "Booking cancelled successfully.")
        else:
            messages.error(
                request,
                "Bookings can only be cancelled more than 24 hours before "
                "check-in."
            )

    return redirect("user_bookings")
