from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, CustomUser, Profile
import re


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user with custom fields."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose a username"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"}
        )

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
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email"
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username"
                }
            ),
        }


class ProfileForm(forms.ModelForm):
    """Form for managing user profile information."""

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        ),
    )

    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter phone number (e.g., +1234567890)",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["phone_number", "address", "date_of_birth"]
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your address"
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }


class BookingForm(forms.ModelForm):
    """Form for creating a new booking with enhanced phone number validation."""
    
    phone_number = forms.CharField(
        required=True,
        max_length=20,  # Give some extra space for formatting
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "email",
            "phone_number",
            "check_in_date",
            "check_out_date",
        ]
        widgets = {
            "guest_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "check_in_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "check_out_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            raise forms.ValidationError("Phone number is required.")
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone_number)
        
        # Check for letters - they are not allowed
        if re.search(r'[a-zA-Z]', phone_number):
            raise forms.ValidationError("Phone number cannot contain letters.")
        
        # Check digit count (between 8 and 12 digits)
        if len(digits_only) < 8 or len(digits_only) > 12:
            raise forms.ValidationError(
                "Phone number must contain between 8 and 12 digits."
            )
        
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError(
                    {
                        "check_out_date":
                        "Check-out date must be after check-in date"
                    }
                )

            if check_in_date < timezone.now().date():
                raise ValidationError(
                    {"check_in_date": "Check-in date cannot be in the past"}
                )

        return cleaned_data


class BookingEditForm(forms.ModelForm):
    """Form for editing existing bookings."""

    check_in_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        )
    )

    check_out_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        )
    )

    status = forms.ChoiceField(
        choices=Booking.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Booking
        fields = ["check_in_date", "check_out_date", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["check_in_date"].initial = self.instance.check_in_date
            self.fields["check_out_date"].initial = self.instance.check_out_date
            self.fields["status"].initial = self.instance.status

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError(
                    {
                        "check_out_date":
                        "Check-out date must be after check-in date"
                    }
                )

            if check_in_date < timezone.now().date():
                raise ValidationError(
                    {"check_in_date": "Check-in date cannot be in the past"}
                )

        return cleaned_data
        
