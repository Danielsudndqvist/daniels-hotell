from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, Booking, Room

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']
        # Note: Removed password field as it should be handled separately for security reasons

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'email', 'phone_number', 'check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError("Check-out date must be after check-in date")
            if check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past")

        return cleaned_data

class BookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'status']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError("Check-out date must be after check-in date")
            if check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past")

        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'room_type', 'price', 'available', 'amenities', 'max_occupancy', 'size']