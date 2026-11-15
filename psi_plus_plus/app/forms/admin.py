import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from app.models import Korisnik, Student

#Autor Artjom Uljanov 2023/0421

class KreiranjeKorisnikaForma(UserCreationForm):
    """
    Forma za registraciju jednog korisnika
    """
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Ime')
    last_name = forms.CharField(max_length=30, required=True, label='Prezime')

    class Meta(UserCreationForm.Meta):
        model = Korisnik
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


INDEKS_PATTERN = re.compile(r"^\d{4}/\d{4}$")


class KreiranjeStudentaForma(forms.ModelForm):
    """
    Forma za registraciju studenta (unos indeksa)
    """
    class Meta:
        model = Student
        fields = ("indeks",)

    def clean_indeks(self):
        indeks = self.cleaned_data["indeks"]
        if not INDEKS_PATTERN.match(indeks):
            raise ValidationError(
                "Indeks mora biti u formatu GGGG/BBBB (npr. 2023/0111).",
                code="invalid_indeks",
            )
        return indeks


class KreiranjeGrupeStudenataForma(forms.Form):
    """
    Forma za registraciju grupe studenata preko .csv fajla
    """
    fajl = forms.FileField(
        validators=[FileExtensionValidator(
            allowed_extensions=['csv'],
            message="Podržane su samo .csv fajlove.",
        )],
        widget=forms.FileInput(attrs={'accept': '.csv'}),
        label="CSV fajl"
    )