import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from rooms.models import Room, Booking, Profile
from rooms.forms import BookingForm


class ViewTests(TestCase):
    """Test cases for view functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.room = Room.objects.create(
            name='Test Room',
            price=Decimal('100.00'),
            room_type='STD',
            available=True
        )

    def test_room_list_view(self):
        """Test the room list view."""
        response = self.client.get(reverse('select_room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'select_room.html')

    def test_book_room_view_authenticated(self):
        """Test booking room view for authenticated users."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('book_room', args=[self.room.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_book_room_view_unauthenticated(self):
        """Test booking room view for unauthenticated users."""
        response = self.client.get(reverse('book_room', args=[self.room.id]))
        login_url = reverse('login')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/book-room/{self.room.id}/',
            fetch_redirect_response=False
        )


class BookingFormTests(TestCase):
    """Test cases for booking form validation."""

    def setUp(self):
        """Set up test data."""
        self.room = Room.objects.create(
            name='Test Room',
            price=Decimal('100.00'),
            room_type='STD',
            available=True
        )

    def test_booking_form_valid(self):
        """Test form validation with valid data."""
        tomorrow = timezone.now().date() + timedelta(days=1)
        data = {
            'guest_name': 'Test Guest',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'check_in_date': tomorrow,
            'check_out_date': tomorrow + timedelta(days=2),
            'room': self.room.id,
        }
        form = BookingForm(data=data)
        form.instance.room = self.room

        if not form.is_valid():
            print("Form errors:", form.errors)

        self.assertTrue(form.is_valid())

    def test_booking_form_invalid_dates(self):
        """Test form validation with invalid dates."""
        tomorrow = timezone.now().date() + timedelta(days=1)
        data = {
            'guest_name': 'Test Guest',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'check_in_date': tomorrow,
            'check_out_date': tomorrow,  # Same date as check-in
            'room': self.room.id,
        }
        form = BookingForm(data=data)
        form.instance.room = self.room
        self.assertFalse(form.is_valid())


class BookingManagementTests(TestCase):
    """Test cases for booking management functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.room = Room.objects.create(
            name='Test Room',
            price=Decimal('100.00'),
            room_type='STD',
            available=True
        )
        future_date = timezone.now().date() + timedelta(days=5)
        self.booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            guest_name='Test Guest',
            email='test@example.com',
            check_in_date=future_date,
            check_out_date=future_date + timedelta(days=2),
            total_price=Decimal('200.00'),
            status='CONFIRMED'
        )

    def test_cancel_booking(self):
        """Test booking cancellation process."""
        self.client.force_login(self.user)

        # Create a future date that's far enough in the future
        future_date = timezone.now().date() + timedelta(days=10)
        print(f"Setting future date: {future_date}")

        self.booking.check_in_date = future_date
        self.booking.check_out_date = future_date + timedelta(days=2)
        self.booking.save()
        print(
            f"Saved booking with check_in_date: {self.booking.check_in_date}"
        )

        # Verify booking exists before cancellation
        booking_id = self.booking.id
        exists_before = Booking.objects.filter(id=booking_id).exists()
        print(f"Booking exists before cancellation: {exists_before}")

        response = self.client.post(
            reverse('cancel_booking', args=[booking_id]),
            follow=True
        )

        # Check response and redirection
        print(f"Response status code: {response.status_code}")
        print(f"Response redirect chain: {response.redirect_chain}")

        # Check if booking still exists
        exists_after = Booking.objects.filter(id=booking_id).exists()
        print(f"Booking exists after cancellation attempt: {exists_after}")

        # Get messages
        messages = list(response.context['messages'])
        print(f"Number of messages: {len(messages)}")
        for message in messages:
            print(f"Message: {message}")
            print(f"Message level: {message.level_tag}")

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('user_bookings'))
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())
