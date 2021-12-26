from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUp(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text=''
    ),
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')