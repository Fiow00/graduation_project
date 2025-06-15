from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from allauth.account.forms import SignupForm
from craftsmen.models import Craftsman
from .models import CustomUser
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

class CustomSignupForm(SignupForm):
    username = forms.CharField(
        max_length=30,
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"})
    )
    phone = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g.: +201234567890 or 01234567890",
            "pattern": r"^(\+20|0)?1[0-9]{9}$",
            "title": "Egyptian number format: +201234567890 or 01234567890",
            "class": "phone-input"  # Added for JavaScript targeting
        }),
        help_text="<small>Enter Egyptian number (e.g.: +201234567890 or 01234567890)</small>",
        validators=[
            RegexValidator(
                regex=r'^(\+20|0)?1[0-9]{9}$',
                message="Enter a valid Egyptian number (+201234567890, 01234567890, or 1234567890)"
            )
        ]
    )
    terms = forms.BooleanField(required=True, label="I Agree To Terms & Conditions.")
    is_craftsman = forms.BooleanField(
        required=False,
        label="Are you a craftsman?",
        help_text="Check this box if you are a craftsman."
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Normalize the phone number format before validation
            phone = phone.strip().replace(' ', '')
            if not phone.startswith(('+20', '0')) and len(phone) == 10:
                phone = f"0{phone}"  # Add leading zero if missing
        return phone

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data["username"]
        user.phone = self.cleaned_data["phone"]
        user.is_craftsman = self.cleaned_data.get("is_craftsman", False)
        user.save()

        if self.cleaned_data.get("is_craftsman"):
            Craftsman.objects.create(user=user)
        return user
