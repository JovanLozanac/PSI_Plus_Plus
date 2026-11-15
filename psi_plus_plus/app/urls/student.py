from django.urls import path

from app.views.student import student_glavna, zahtev_poslat, pravljenje_tima, azuriranje_tima, prikaz_zahteva, \
    obrada_zahteva, cuvanje_projekta

#Autor Jovan Lozanac 2023/0084
#Autor Luka Milic 2022/0182

app_name = 'student'

urlpatterns = [
    path('', student_glavna, name='glavna'),
    path('zahtev_poslat', zahtev_poslat, name='zahtev'),
    path('pravljenje_tima', pravljenje_tima, name='pravljenje_tima'),
    path('azuriranje_tima', azuriranje_tima, name='azuriranje_tima'),
    path('prikaz_zahteva', prikaz_zahteva, name='prikaz_zahteva'),
    path('obrada_zahteva/<int:korid>', obrada_zahteva, name='obrada_zahteva'),
    path('cuvanje_projekta', cuvanje_projekta, name='cuvanje_projekta'),
]
