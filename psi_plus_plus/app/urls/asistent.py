from django.urls import path

from app.views.asistent import asistent_glavna, kreiranje_obavestenja, kreiranje_zadatka, tabela_resenja, prikaz_resenja_zadatka, asistent_preuzimanje_zadatka, ocenjivanje_resenja

#Autor Luka Milic 2022/0182
#Autor Jovan Lozanac 2023/0084
#Autor David Radivojevic 2021/0504

app_name = 'asistent'

urlpatterns = [
    path('', asistent_glavna, name='glavna'),
    path('kreiranje_obavestenja', kreiranje_obavestenja, name='kreiranje_obavestenja'),
    path('kreiranje_zadatka', kreiranje_zadatka, name='kreiranje_zadatka'),
    path('tabela_resenja/<int:zad_id>', tabela_resenja, name='tabela_resenja'),
    path('prikaz_resenja_zadatka/<int:tim_id>/<int:zad_id>', prikaz_resenja_zadatka, name="prikaz_resenja_zadatka"),
    path('preuzimanje_projekta/<int:timid>/<int:zadid>', asistent_preuzimanje_zadatka, name='preuzimanje_projekta'),
    path('ocenjivanje_resenja/<int:tim_id>/<int:zad_id>', ocenjivanje_resenja, name='ocenjivanje_resenja')
]
