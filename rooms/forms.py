from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
import re


from .models import Booking, CustomUser, Profile, Room


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with custom fields."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter password"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password"
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    """Form for updating user information."""

    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your username"
            })
        }


class ProfileForm(forms.ModelForm):
    """Form for managing user profile information."""

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        )
    )

    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter phone number (e.g., +1234567890)"
        })
    )

    class Meta:
        model = Profile
        fields = ["phone_number", "address", "date_of_birth"]
        widgets = {
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your address"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            })
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'email', 'phone_number', 'check_in_date', 'check_out_date']
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Remove any non-digit characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            # Check if the phone number has a valid length (adjust as needed)
            if len(phone_number) < 10 or len(phone_number) > 15:
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone_number

class BookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "email",
            "phone_number",
            "check_in_date",
            "check_out_date"
        ]
        widgets = {
            "guest_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter guest name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text and error messages
        self.fields["guest_name"].error_messages = {
            "required": "Please enter the guest name"
        }
        self.fields["email"].error_messages = {
            "required": "Please enter an email address",
            "invalid": "Please enter a valid email address"
        }
        self.fields['phone_number'].error_messages.update({
            'required': 'Phone number is required',
            'invalid': 'Please enter a valid phone number'
        })
        self.fields["check_in_date"].error_messages = {
            "required": "Please select a check-in date"
        }
        self.fields["check_out_date"].error_messages = {
            "required": "Please select a check-out date"
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError({
                    "check_out_date":
                    f"Check-out date must be after check-in date"
                })

            if check_in_date < timezone.now().date():
                raise ValidationError({
                    "check_in_date":
                    f"Check-in date cannot be in the past"
                })

            min_stay = 1
            if (check_out_date - check_in_date).days < min_stay:
                raise ValidationError({
                    "check_out_date": f"Minimum stay is {min_stay} night(s)"
                })

        return cleaned_data


class BookingEditForm(forms.ModelForm):
    """Form for editing existing bookings."""

    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    status = forms.ChoiceField(
        choices=Booking.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Booking
        fields = ["check_in_date", "check_out_date", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["check_in_date"].initial = (
                self.instance.check_in_date
            )
            self.fields["check_out_date"].initial = (
                self.instance.check_out_date
            )
            self.fields["status"].initial = self.instance.status

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError({
                    "check_out_date":
                    f"Check-out date must be after check-in date"
                    })

            if check_in_date < timezone.now().date():
                raise ValidationError({
                    "check_in_date": "Check-in date cannot be in the past"
                })

        return cleaned_data


class RoomForm(forms.ModelForm):
    """Form for managing room information."""

    class Meta:
        model = Room
        fields = [
            "name",
            "description",
            "room_type",
            "price",
            "available",
            "amenities",
            "max_occupancy",
            "size"
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter room name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter room description",
                "rows": 3
            }),
            "room_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01"
            }),
            "available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "amenities": forms.SelectMultiple(attrs={
                "class": "form-control"
            }),
            "max_occupancy": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1"
            }),
            "size": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            })
        }
