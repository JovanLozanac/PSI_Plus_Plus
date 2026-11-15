from django import forms
from django.contrib.auth.forms import AuthenticationForm

#Autor Artjom Uljanov 2023/0421

class LoginForm(AuthenticationForm):
    """
    Forma za prijavu korisnika
    """
    username = forms.CharField(
        label='Korisničko ime',
        widget=forms.TextInput(attrs={
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Lozinka',
        widget=forms.PasswordInput(attrs={
        })
    )