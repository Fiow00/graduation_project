from django import forms
from django.contrib.auth import get_user_model
from craftsmen.models import Craftsman

CustomUser = get_user_model()

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["photo", "username", "email", "governorate", "city"]

class CraftsmanProfileUpdateForm(forms.ModelForm):
    # Add fields from the CustomUser model
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Craftsman
        fields = ["photo", "service", "governorate", "city"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the form with data from the CustomUser model
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        craftsman = super().save(commit=False)
        # Update the CustomUser fields
        if self.cleaned_data.get('username'):
            craftsman.user.username = self.cleaned_data['username']
        if self.cleaned_data.get('email'):
            craftsman.user.email = self.cleaned_data['email']
        if commit:
            craftsman.user.save()
            craftsman.save()
        return craftsman