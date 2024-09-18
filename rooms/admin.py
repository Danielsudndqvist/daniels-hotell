from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Room, Booking

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'date_of_birth')
    search_fields = ('user__username',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price', 'available')
    list_filter = ('room_type', 'available')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'room')
    search_fields = ('guest_name', 'room__name')
