from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom user model extending Django's AbstractUser
class CustomUser(AbstractUser):
    # Email field must be unique
    email = models.EmailField(unique=True)

    # Set email as the username field for authentication
    USERNAME_FIELD = "email"
    # Specify that username is a required field
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        # Return the email for string representation
        return self.email


# Profile model to store additional information about the user
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Link to the CustomUser model
    phone_number = models.CharField(
        max_length=15, blank=True, null=True
    )  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address field
    date_of_birth = models.DateField(
        blank=True, null=True
    )  # Optional date of birth

    def __str__(self):
        # Return the username associated with the profile
        return f"{self.user.username}'s profile"


# Model representing various amenities available for rooms
class Amenity(models.Model):
    name = models.CharField(max_length=50)  # Name of the amenity

    def __str__(self):
        # Return the amenity name for string representation
        return self.name

    class Meta:
        # Specify the plural name for the model
        verbose_name_plural = "Amenities"


# Model representing a room in the hotel
class Room(models.Model):
    name = models.CharField(max_length=100)  # Room name
    description = models.TextField()  # Description of the room
    # Choices for room types
    ROOM_TYPES = [
        ("STD", "Standard"),
        ("DLX", "Deluxe"),
        ("SUI", "Suite"),
    ]
    room_type = models.CharField(
        max_length=3, choices=ROOM_TYPES
    )  # Room type selection
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Room price per night
    available = models.BooleanField(
        default=True
    )  # Availability status of the room
    amenities = models.ManyToManyField(
        Amenity, blank=True
    )  # Relationship to amenities (many-to-many)
    max_occupancy = models.IntegerField(default=2)  # Maximum number of guests
    size = models.IntegerField(
        help_text="Size in square feet", default=0
    )  # Size of the room in square feet

    def __str__(self):
        # Return the room name for string representation
        return self.name


# Model for storing images associated with rooms
class RoomImage(models.Model):
    room = models.ForeignKey(
        Room, related_name="images", on_delete=models.CASCADE
    )  # Link to the Room model
    image = models.ImageField(
        upload_to="room_images/"
    )  # Image field for room images
    caption = models.CharField(
        max_length=100, blank=True
    )  # Optional caption for the image

    def __str__(self):
        # Return a description of the image related to the room
        return f"Image for {self.room.name}"


# Model representing a booking made by a user
class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  # Link to the user making the booking
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )  # Link to the room being booked
    guest_name = models.CharField(max_length=100)  # Name of the guest
    email = models.EmailField()  # Email of the guest
    phone_number = models.CharField(
        max_length=15, blank=True, null=True
    )  # Optional phone number
    check_in_date = models.DateField()  # Check-in date for the booking
    check_out_date = models.DateField()  # Check-out date for the booking
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Total price for the booking
    # Choices for the status of the booking
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )  # Current status of the booking

    def __str__(self):
        # Return a description of the booking
        # including the room name and guest name
        return f"Booking for {self.room.name} by {self.guest_name}"
