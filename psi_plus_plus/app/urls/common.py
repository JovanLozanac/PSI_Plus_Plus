from django.urls import path
from django.contrib.auth import views as auth_views

from app.forms.common import LoginForm
from app.views.common import homepage_dispatcher, profil_korisnika, lista_timova, prikaz_tima, promena_lozinke, prikaz_obavestenja, prikaz_fajla, prikaz_direktorijuma, preuzimanje_projekta
#Autor Jovan Lozanac 2023/0084
#Autor Luka Milic 2022/0182
#Autor Artjom Uljanov 2023/0421
#Autor David Radivojevic 2021/0504

urlpatterns = [
    path('', homepage_dispatcher, name='homepage'),
    path('prijava', auth_views.LoginView.as_view(
        template_name='app/prijava.html',
        authentication_form=LoginForm,
    ), name='prijava'),
    path('odjava/', auth_views.LogoutView.as_view(), name='odjava'),
    path('profil/', profil_korisnika, name='profil'),
    path('promena_lozinke/', promena_lozinke, name='promena_lozinke'),
    path('lista_timova', lista_timova, name='lista_timova'),
    path('prikaz_tima/<int:timid>', prikaz_tima, name='prikaz_tima'),
    path('prikaz_obavestenja', prikaz_obavestenja, name='prikaz_obavestenja'),
    path('prikaz_direktorijuma/<int:timid>', prikaz_direktorijuma, name='prikaz_direktorijuma'),
    path('prikaz_fajla/<int:timid>', prikaz_fajla, name='prikaz_fajla'),
    path('preuzimanje_projekta/<int:timid>', preuzimanje_projekta, name='preuzimanje_projekta'),
]