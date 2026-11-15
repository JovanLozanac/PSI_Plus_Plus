from django.urls import path

from app.views.admin import (
    admin_glavna,
    obrisi_korisnika,
    brisanje_svih_studenata,
    registracija_korisnika,
    registracija_grupe_studenata,
)

#Autor Artjom Uljanov 2023/0421

app_name = 'upravljanje'

urlpatterns = [
    path('', admin_glavna, name='glavna'),
    path('korisnik/<int:korid>/obrisi', obrisi_korisnika, name='obrisi_korisnika'),
    path('studenti/brisanje', brisanje_svih_studenata, name='brisanje_svih_studenata'),
    path('korisnik/registracija', registracija_korisnika, name='registracija_korisnika'),
    path('korisnik/registracija_grupe_studenata', registracija_grupe_studenata, name='registracija_grupe_studenata'),
]