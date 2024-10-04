from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ROOM_TYPES = [
        ('STD', 'Standard'),
        ('DLX', 'Deluxe'),
        ('SUI', 'Suite'),
    ]
    room_type = models.CharField(max_length=3, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    max_occupancy = models.IntegerField(default=2)
    size = models.IntegerField(help_text="Size in square feet", default=0)

    def __str__(self):
        return self.name

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.room.name}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Booking for {self.room.name} by {self.guest_name}"