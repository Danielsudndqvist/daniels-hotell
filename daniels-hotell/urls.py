from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rooms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('rooms/', views.select_room, name='rooms'),
    path('select-room/', views.select_room, name='select_room'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('room-details/<int:room_id>/', views.room_details, name='room_details'),
    path('search/', views.search_rooms, name='search_rooms'),  
    path('amenities/', views.amenities_list, name='amenities_list'),  
    path('my-bookings/', views.user_bookings, name='user_bookings'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)