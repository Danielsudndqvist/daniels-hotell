from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Booking, CustomUser, Profile


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
    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "email",
            "phone_number",
            "check_in_date",
        ]
