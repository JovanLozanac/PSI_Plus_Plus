from django import forms
from app.models import Obavestenje, Zadatak, Ocena
#Autor Luka Milic 2022/0182
#Autor David Radivojevic 2021/0504

class ObavestenjeForma(forms.ModelForm):
    """
    Klasa koja definise html formu za unos obavestenja
    """
    class Meta:
        """
        Unutrasnja klasa definise organizaciju forme na osnovu modela
        """
        model = Obavestenje
        fields = ['naslov', 'tekst']
        exclude = ['korid']
        widgets = {
            'tekst': forms.Textarea(attrs={
                'rows': 5,
                'cols': 40
            })
        }


class ZadatakForma(forms.ModelForm):
    """
    Klasa koja definise html formu za unos zadatka
    """
    class Meta:
        """
        Unutrasnja klasa definise organizaciju forme na osnovu modela
        """
        model = Zadatak
        fields = ['rok', 'naslov', 'tekst', 'brfaze']
        exclude = ['korid']
        widgets = {
            'tekst': forms.Textarea(attrs={
                'rows': 5,
                'cols': 40
            }),
            'rok': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            })
        }
        labels = {
            'brfaze': 'Broj faze'
        }

class OceniZadatakForma(forms.ModelForm):
    """
    Forma koja se prikazuje pri ocenjivanju zadatka
    """
    class Meta:
        model = Ocena
        fields = ['bodovi', 'komentar']
        exclude = ['ocid', 'zadid', 'timid', 'korid']

        widgets = {
            'bodovi': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '-100',
                'max': '100'
            }),
            'komentar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'cols': 40,
                'placeholder': "Unesite obrazlozenje ocene..."
            })
        }

        labels = {
            'bodovi': 'Osvojeni bodovi',
            'komentar': "Komentar asistenta"
        }