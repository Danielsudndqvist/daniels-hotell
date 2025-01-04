from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from rooms.models import Room, Booking, Amenity, Profile
from rooms.forms import BookingForm

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
           size=300,
           available=True
       )
       self.room.amenities.add(self.amenity)

   def test_room_creation(self):
       self.assertEqual(str(self.room), 'Deluxe Room')
       self.assertEqual(self.room.amenities.count(), 1)
       self.assertEqual(self.room.amenities.first().name, 'TV')

class ViewTests(TestCase):
   def setUp(self):
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
       response = self.client.get(reverse('select_room'))
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'select_room.html')

   def test_book_room_view_authenticated(self):
       self.client.login(username='testuser', password='testpass123')
       
       select_room_response = self.client.get(
           reverse('select_room'),
           {'check_in': '2025-01-10', 'check_out': '2025-01-12'}
       )
       
       book_response = self.client.get(
           reverse('book_room', args=[self.room.id]),
           follow=True
       )
       
       self.assertEqual(book_response.status_code, 200)

   def test_book_room_view_unauthenticated(self):
       response = self.client.get(reverse('book_room', args=[self.room.id]))
       login_url = reverse('login')
       self.assertRedirects(response, f'{login_url}?next=/book-room/{self.room.id}/')

class BookingManagementTests(TestCase):
   def setUp(self):
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
       self.booking = Booking.objects.create(
           room=self.room,
           user=self.user,
           guest_name='Test Guest',
           email='test@example.com',
           check_in_date='2025-01-10',
           check_out_date='2025-01-12',
           total_price=Decimal('200.00'),
           status='CONFIRMED'
       )

   def test_edit_booking(self):
       self.client.login(username='testuser', password='testpass123')
       
       new_check_in = '2025-01-10'
       new_check_out = '2025-01-12'
       
       form_data = {
           'check_in_date': new_check_in,
           'check_out_date': new_check_out,
           'status': self.booking.status
       }
       
       response = self.client.post(
           reverse('edit_booking', args=[self.booking.id]),
           form_data,
           follow=True
       )
       
       self.booking.refresh_from_db()
       self.assertEqual(
           self.booking.check_in_date.strftime('%Y-%m-%d'),
           new_check_in
       )
       self.assertEqual(
           self.booking.check_out_date.strftime('%Y-%m-%d'),
           new_check_out
       )

   def test_cancel_booking(self):
    # Log in the user using force_login
    self.client.force_login(self.user)
    print(f"Is user logged in? {self.client.session.get('_auth_user_id')}")
    
    # Set future date
    future_date = timezone.now().date() + timezone.timedelta(days=5)
    print(f"Future date in test: {future_date}")
    self.booking.check_in_date = future_date
    self.booking.check_out_date = future_date + timezone.timedelta(days=2)
    self.booking.status = 'CONFIRMED'
    self.booking.save()
    print(f"Booking check_in_date in test: {self.booking.check_in_date}")
    
    # Cancel booking
    response = self.client.post(
        reverse('cancel_booking', args=[self.booking.id]),
        follow=True
    )
    
    # Check response status code and redirection
    self.assertEqual(response.status_code, 200)
    self.assertRedirects(response, reverse('user_bookings'))
    self.assertTemplateUsed(response, 'user_bookings.html')
    
    # Check messages
    messages = list(response.context['messages'])
    self.assertEqual(len(messages), 1)
    self.assertEqual(str(messages[0]), 'Booking cancelled successfully.')
    
    # Refresh booking from database and verify status
    self.booking.refresh_from_db()
    self.assertEqual(self.booking.status, 'CANCELLED')

    
class BookingFormTests(TestCase):
   def setUp(self):
       self.room = Room.objects.create(
           name='Test Room',
           price=Decimal('100.00'),
           room_type='STD',
           available=True
       )
       self.valid_data = {
           'guest_name': 'Test Guest',
           'email': 'test@example.com',
           'phone_number': '+1234567890',
           'check_in_date': '2025-01-10',
           'check_out_date': '2025-01-12'
       }

   def test_booking_form_valid(self):
       form = BookingForm(data=self.valid_data)
       self.assertTrue(form.is_valid())

   def test_booking_form_invalid_dates(self):
       invalid_data = self.valid_data.copy()
       invalid_data['check_out_date'] = invalid_data['check_in_date']
       form = BookingForm(data=invalid_data)
       self.assertFalse(form.is_valid())