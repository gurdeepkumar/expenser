from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check for only alphabets and minimum length of 8 characters
        if not re.match(r"^[a-zA-Z]+$", username):
            raise forms.ValidationError("Username must contain only alphabets.")
        if len(username) < 6:
            raise forms.ValidationError("Username must be at least 6 characters long.")
        return username
