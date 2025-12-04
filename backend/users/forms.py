from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    """."""

    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(
            attrs={
                'class': 'forms-input',
                'placeholder': 'Enter username or email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Enter password'
            }
        )
    )
