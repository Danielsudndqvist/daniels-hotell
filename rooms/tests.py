import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rooms.models import Profile, Amenity, Room, RoomImage, Booking
from django.utils import timezone
from decimal import Decimal

class CustomUserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', username='testuser', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', username='testsuperuser', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class ProfileModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, phone_number='1234567890', address='123 Test St')
        self.assertEqual(str(profile), "testuser's profile")
        self.assertEqual(profile.user.email, 'test@example.com')

class AmenityModelTests(TestCase):
    def test_amenity_creation(self):
        amenity = Amenity.objects.create(name='Wi-Fi')
        self.assertEqual(str(amenity), 'Wi-Fi')

class RoomModelTests(TestCase):
    def setUp(self):
        self.amenity = Amenity.objects.create(name='TV')
        self.room = Room.objects.create(
            name='Deluxe Room',
            description='A luxurious room',
            room_type='DLX',
            price=Decimal('200.00'),
            max_occupancy=2,
            size=300
        )
        self.room.amenities.add(self.amenity)

    def test_room_creation(self):
        self.assertEqual(str(self.room), 'Deluxe Room')
        self.assertEqual(self.room.amenities.count(), 1)
        self.assertEqual(self.room.amenities.first().name, 'TV')

class BookingModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.room = Room.objects.create(
            name='Standard Room',
            description='A standard room',
            room_type='STD',
            price=Decimal('100.00'),
            max_occupancy=2,
            size=200
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            guest_name='John Doe',
            email='john@example.com',
            check_in_date=timezone.now().date(),
            check_out_date=timezone.now().date() + timezone.timedelta(days=1),
            total_price=Decimal('100.00')
        )
        self.assertEqual(str(booking), 'Booking for Standard Room by John Doe')
        self.assertEqual(booking.status, 'PENDING')

@pytest.mark.django_db
def test_room_availability():
    room = Room.objects.create(name='Test Room', room_type='STD', price=100, available=True)
    assert room.available == True
    room.available = False
    room.save()
    assert room.available == False

@pytest.mark.django_db
def test_booking_date_validation():
    room = Room.objects.create(name='Test Room', room_type='STD', price=100)
    with pytest.raises(ValidationError):
        Booking.objects.create(
            room=room,
            guest_name='Test Guest',
            email='test@example.com',
            check_in_date=timezone.now().date(),
            check_out_date=timezone.now().date() - timezone.timedelta(days=1),
            total_price=100
        )