from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, Profile

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active') 
    search_fields = ('email', 'username')
    filter_horizontal = ()
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.profile_picture.url if obj.profile.profile_picture else ''
        return ''

    get_profile.short_description = 'Profile Picture URL'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if hasattr(obj, 'profile'):
            obj.profile.save()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
