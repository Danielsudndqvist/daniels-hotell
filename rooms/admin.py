from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Amenity, Booking, CustomUser, Profile, Room, RoomImage


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "address", "date_of_birth")
    search_fields = ("user__username", "user__email", "phone_number")


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "room_type",
        "price",
        "available",
        "max_occupancy",
        "size",
    )
    list_filter = ("room_type", "available")
    search_fields = ("name", "description")
    inlines = [RoomImageInline]
    filter_horizontal = ("amenities",)


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ("room", "caption", "image")
    list_filter = ("room",)
    search_fields = ("room__name", "caption")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "guest_name",
        "check_in_date",
        "check_out_date",
        "total_price",
        "status",
    )
    list_filter = ("status", "room", "check_in_date", "check_out_date")
    search_fields = ("guest_name", "room__name", "email")
    date_hierarchy = "check_in_date"


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
