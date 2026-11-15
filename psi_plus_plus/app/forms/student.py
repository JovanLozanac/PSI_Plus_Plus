from django import forms
from app.models import Tim
#Autor Luka Milic 2022/0182

class TimForma(forms.ModelForm):
    """
    Klasa koja definise html formu za unos tima
    """
    class Meta:
        model = Tim
        fields = ['nazivtima']
        exclude = ['timid', 'imeprojekta', 'opisprojekta']

        labels = {
            'nazivtima': 'Naziv tima'
        }


class UpdateTimForma(forms.ModelForm):
    """
    Klasa koja definise html formu za azuriranje tima
    """
    class Meta:
        model = Tim
        fields = ['nazivtima', 'imeprojekta', 'opisprojekta']
        exclude = ['timid']

        labels = {
            'nazivtima': 'Naziv tima',
            'imeprojekta': 'Naziv projekta',
            'opisprojekta': 'Opis projekta'
        }

        widgets = {
            'opisprojekta': forms.Textarea(attrs={
                'rows': 10
            })
        }

    def validate_unique(self):
        """
        Redefinicija jedinstvenosti jer naziv tima sme da bude isti
        prethodnoj vrednosti.
        """
        pass
