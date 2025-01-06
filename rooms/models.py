from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ROOM_TYPES = [
        ("STD", "Standard"),
        ("DLX", "Deluxe"),
        ("SUI", "Suite"),
    ]
    room_type = models.CharField(max_length=3, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    max_occupancy = models.IntegerField(default=2)
    size = models.IntegerField(help_text="Size in square feet", default=0)

    def clean(self):
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
        return self.images.first()


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE)
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
        try:
            return self.image.url
        except:
            return None

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images of this room to not primary
            RoomImage.objects.filter(room=self.room).update(is_primary=False)
        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
    
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    def clean(self):
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date")
        
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        ).exclude(id=self.id)  # Exclude current booking when updating
        
        if overlapping_bookings.exists():
            raise ValidationError("Room is already booked for these dates")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.room.name} by {self.guest_name}"
        