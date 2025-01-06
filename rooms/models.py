from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUser(AbstractUser):
    """Custom user model with email as the username field."""

    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    """User profile model containing additional user information."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



class Room(models.Model):
    """Model representing a hotel room."""

    ROOM_TYPES = [
        ("STD", "Standard"),
        ("DLX", "Deluxe"),
        ("SUI", "Suite"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    room_type = models.CharField(max_length=3, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    max_occupancy = models.IntegerField(default=2)
    size = models.IntegerField(help_text="Size in square feet", default=0)

    def clean(self):
        """Validate room attributes."""
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.max_occupancy < 1:
            raise ValidationError("Maximum occupancy must be at least 1")
        if self.size < 0:
            raise ValidationError("Room size cannot be negative")

    def __str__(self):
        return self.name

    @property
    def primary_image(self):
        """Get the first image associated with the room."""
        return self.images.first()


class RoomImage(models.Model):
    """Model for room images."""

    room = models.ForeignKey(
        Room, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="room_images/")
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.room.name}"

    @property
    def image_url(self):
        """Get the URL of the image, return None if not available."""
        try:
            return self.image.url
        except Exception:
            return None

    def set_as_primary(self):
        """Set this image as primary for its room."""
        RoomImage.objects.filter(room=self.room, is_primary=True).update(is_primary=False)
        self.is_primary = True
        self.save()

    @classmethod
    def update_primary_image(cls, room_id):
        """Update primary image for a specific room."""
        try:
            room = Room.objects.get(id=room_id)
            images = list(room.images.all())
            
            if images:
                # Sort images by order
                images.sort(key=lambda x: x.order)
                
                # Set all other images as non-primary
                cls.objects.filter(room=room).exclude(pk=images[0].pk).update(is_primary=False)
                
                # Set first image as primary
                images[0].set_as_primary()
            else:
                print(f"No images found for room {room_id}")
        except Room.DoesNotExist:
            print(f"Room with id {room_id} does not exist")

    def delete(self, *args, **kwargs):
        """Override delete method to handle GCS deletion."""
        super().delete(*args, **kwargs)
        default_storage.delete(self.image.path)

    def save(self, *args, **kwargs):
        """Override save method to handle GCS storage."""
        super().save(*args, **kwargs)
        
        # Update order if necessary
        RoomImage.objects.filter(room=self.room).order_by('order').update(order=models.F('id'))
        


class Booking(models.Model):
    """Model for room bookings."""

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )

    def clean(self):
        """Validate booking dates and availability."""
        super().clean()

        if not all([self.check_in_date, self.check_out_date]):
            raise ValidationError('Check-in and check-out dates must be complete.')

        if self.check_in_date and self.check_out_date:
            if self.check_in_date >= self.check_out_date:
                raise ValidationError('Check-out date must be after check-in date')

            if self.check_in_date < timezone.now().date():
                raise ValidationError('Check-in date cannot be in the past')

        if hasattr(self, 'room') and self.room is not None:
            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                check_in_date__lt=self.check_out_date,
                check_out_date__gt=self.check_in_date
            )

            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError('Room is already booked for these dates')

    def save(self, *args, **kwargs):
        """Override save to perform full validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.room.name} by {self.guest_name}"
