from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,

)
from django import forms


class CustomAuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Your username",
            "class": "form__input",
            "id": 'login_id_username',
        }),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "Your password",
            "class": "form__input",
            "id": 'login_id_password',
        }),
    )


class CustomUserCreationForm(UserCreationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your username",
            "class": "form__input",
            "id": 'registration_id_username',
        }),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        help_text='Enter the password.',
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Enter a new password",
            "class": "form__input",
            "id": 'registration_id_password1',
        }),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Confirm a new password",
            "class": "form__input",
            "id": 'registration_id_password2',
        }),
    )
