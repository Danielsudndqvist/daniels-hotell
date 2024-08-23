from django.db import models

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('DLX', 'Deluxe'),
        ('SLDX', 'Super Deluxe'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    room_type = models.CharField(max_length=6, choices=ROOM_TYPES)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name