from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    full_name        = forms.CharField(max_length=150, label="Full Name")
    email            = forms.EmailField(label="Email")
    password         = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pw and cpw and pw != cpw:
            raise forms.ValidationError("Passwords do not match")
        if User.objects.filter(username=cleaned.get("email")).exists():
            raise forms.ValidationError("Email already registered")
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username   = data["email"],
            email      = data["email"],
            password   = data["password"],
            first_name = data["full_name"]
        )
        return user