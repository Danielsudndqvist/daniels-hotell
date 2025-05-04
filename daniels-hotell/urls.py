from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rooms import views as rooms_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", rooms_views.home, name="home"),
    # Room URLs
    path("rooms/", rooms_views.room_list, name="room_list"),
    path("select-room/", rooms_views.room_list, name="select_room"),
    path("room/<int:room_id>/", rooms_views.room_detail, name="room_detail"),
    path("room-details/<int:room_id>/", rooms_views.room_details, name="room_details"),
    path(
        "room-details-json/<int:room_id>/",
        rooms_views.room_details_json,
        name="room_details_json",
    ),
    path("search-rooms/", rooms_views.search_rooms, name="search_rooms"),
    path(
        "check-availability/", rooms_views.check_availability, name="check_availability"
    ),
    # Booking URLs
    path("book-room/<int:room_id>/", rooms_views.book_room, name="book_room"),
    path(
        "booking-confirmation/<int:booking_id>/",
        rooms_views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("my-bookings/", rooms_views.user_bookings, name="user_bookings"),
    path(
        "edit-booking/<int:booking_id>/", rooms_views.edit_booking, name="edit_booking"
    ),
    path(
        "cancel-booking/<int:booking_id>/",
        rooms_views.cancel_booking,
        name="cancel_booking",
    ),
    # Authentication URLs
    path("login/", rooms_views.login_view, name="login"),
    path("logout/", rooms_views.logout_view, name="logout"),
    path("register/", rooms_views.register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
