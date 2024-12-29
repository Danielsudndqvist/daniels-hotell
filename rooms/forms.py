from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser, Profile, Booking, Room

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

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
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            })
        }

class ProfileForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number (e.g., +1234567890)'
        })
    )

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

class BookingForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17
    )

    class Meta:
        model = Booking
        fields = ['guest_name', 'email', 'phone_number', 'check_in_date', 'check_out_date']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guest name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number (e.g., +1234567890)'
            }),
            'check_in_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'check_out_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError({
                    'check_out_date': "Check-out date must be after check-in date"
                })
            
            if check_in_date < timezone.now().date():
                raise ValidationError({
                    'check_in_date': "Check-in date cannot be in the past"
                })

            # Add minimum stay validation (optional)
            min_stay = 1  # minimum stay in days
            if (check_out_date - check_in_date).days < min_stay:
                raise ValidationError({
                    'check_out_date': f"Minimum stay is {min_stay} night(s)"
                })

        return cleaned_data

class BookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'status']
        widgets = {
            'check_in_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'check_out_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise ValidationError({
                    'check_out_date': "Check-out date must be after check-in date"
                })
            
            current_date = timezone.now().date()
            if check_in_date < current_date:
                raise ValidationError({
                    'check_in_date': "Check-in date cannot be in the past"
                })

        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'room_type', 'price', 'available', 'amenities', 'max_occupancy', 'size']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room description',
                'rows': 3
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'amenities': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'max_occupancy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }
