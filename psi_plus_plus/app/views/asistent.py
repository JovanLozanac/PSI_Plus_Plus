import io
import zipfile

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction

from app.permissions import role_required, ASISTENT
from app.forms.asistent import ObavestenjeForma, ZadatakForma, OceniZadatakForma
from app.models import Obavestenje, Primio, Korisnik, Zadatak, Asistent, Tim, UTimu, Projekat, Ocena
from app.views.common import projekti_path, dohvati_obavestenja, dohvati_projekat

from pathlib import Path

#Autor Luka Milic 2022/0182
#Autor Jovan Lozanac 2023/0084
#Autor David Radivojevic 2021/0504

@role_required(ASISTENT)
def asistent_glavna(request):
    """
    View na glavnu stranicu asistenta
    """
    zadaci = Zadatak.objects.all()
    obavestenja = dohvati_obavestenja(request.user)
    context = {
        'zadaci': zadaci,
        'obavestenja': obavestenja
    }
    return render(request, 'app/asistent/glavna.html', context)


@role_required(ASISTENT)
def kreiranje_obavestenja(request):
    """
    Ako request ima GET metodu ova funkcija vraca stranicu za kreiranje obavestenja.
    Ako request ima POST metodu ova funkcija upisuje dato obavestenje u bazu i
    poziva redirect za glavnu stranicu asistenta.
    """
    if request.method == 'POST':
        form = ObavestenjeForma(request.POST)
        if form.is_valid():
            with transaction.atomic():
                novo_obavestenje = Obavestenje.objects.create(naslov=form.cleaned_data['naslov'], tekst=form.cleaned_data['tekst'], korid=request.user)
                korisnici = Korisnik.objects.all()
                for korisnik in korisnici:
                    Primio.objects.create(korid=korisnik, obid=novo_obavestenje)
            return redirect('asistent:glavna')
    return render(request, 'app/asistent/kreiranje_obavestenja.html', {'form': ObavestenjeForma()})


@role_required(ASISTENT)
def kreiranje_zadatka(request):
    """
    Ako request ima GET metodu ova funkcija vraca stranicu za kreiranje zadatka.
    Ako request ima POST metodu ova funkcija upisuje dat zadatak u bazu i
    poziva redirect za glavnu stranicu asistenta.
    """
    if request.method == 'POST':
        form = ZadatakForma(request.POST)
        if form.is_valid():
            asistent = Asistent.objects.get(korid=request.user)
            with transaction.atomic():
                zadatak = Zadatak.objects.create(rok=form.cleaned_data['rok'],
                                       naslov=form.cleaned_data['naslov'],
                                       tekst=form.cleaned_data['tekst'],
                                       brfaze=form.cleaned_data['brfaze'],
                                       korid=asistent)
                novo_obavestenje = Obavestenje.objects.create(naslov=form.cleaned_data['naslov'], tekst=form.cleaned_data['tekst'], korid=request.user)
                korisnici = Korisnik.objects.all()
                for korisnik in korisnici:
                    if korisnik.je_student:
                        Primio.objects.create(korid=korisnik, obid=novo_obavestenje)
                if zadatak.brfaze != 0:
                    Path(f'{projekti_path}/zadatak_{zadatak.zadid}').mkdir(exist_ok=True)
                    timovi = Tim.objects.all()
                    for tim in timovi:
                        Path(f'{projekti_path}/zadatak_{zadatak.zadid}/tim_{tim.timid}').mkdir(exist_ok=True)
            return redirect('asistent:glavna')
    return render(request, 'app/asistent/kreiranje_zadatka.html', {'form': ZadatakForma()})


@role_required(ASISTENT)
def tabela_resenja(request, zad_id):
    """
    Funkcija koja preusmerava asistenta na tabelu sa resenjima svih timova za neki zadatak
    """
    zadatak = Zadatak.objects.filter(zadid=zad_id).first()

    svi_timovi = Tim.objects.all()

    podaci = []

    for tim in svi_timovi:
        broj_clanova = UTimu.objects.filter(timid=tim.timid).count()
        putanja = f"{projekti_path}/zadatak_{zad_id}/tim_{tim.timid}"
        projekat = Projekat.objects.filter(folder=putanja).first()

        tim_info = {
            "timid": tim.timid,
            "ime_tima": tim.nazivtima,
            "broj_clanova": broj_clanova,
            "predao": projekat is not None,
            "datum_predaje": projekat.updatum if projekat else None,
            "projekat_putanja": putanja if projekat else None
        }

        podaci.append(tim_info)

    context = {
        'zadatak': zadatak,
        'podaci': podaci,
    }

    return render(request, 'app/asistent/tabela_resenja.html', context)


@role_required(ASISTENT)
def prikaz_resenja_zadatka(request, tim_id, zad_id):
    """
    Funkcija koja prikazuje resenje jednog tima za jedan zadatak
    """
    projekat_info = Tim.objects.filter(timid=tim_id).first()
    zadatak = Zadatak.objects.filter(zadid=zad_id).first()

    ocena = Ocena.objects.filter(timid=tim_id, zadid=zad_id)

    sadrzaj = dohvati_projekat(tim_id, zad_id)

    context = {
        'projekat_info': projekat_info,
        'sadrzaj': sadrzaj,
        'zadatak': zadatak,
        'ocena' : ocena
    }

    return render(request, 'app/asistent/prikaz_resenja_zadatka.html', context)

@role_required(ASISTENT)
def asistent_preuzimanje_zadatka(request, timid, zadid):
    """
    Zipuje projekat tima iz foldera projekti/zadatak_<zad_id>_/tim_<timid>
    i vraca ga asistentu na preuzimanje.
    """
    zadatak = Zadatak.objects.filter(zadid=zadid).first()
    tim = Tim.objects.filter(timid=timid).first()
    folder = f'{projekti_path}/zadatak_{zadatak.zadid}/tim_{tim.timid}'
    path = Path(folder)
    if not path.exists():
        raise Http404('Projekat nije pronađen.')

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in path.rglob('*'):
            if file_path.is_file():
                zip_file.write(file_path, file_path.relative_to(path))
    buffer.seek(0)

    naziv_fajla = f'zadatak_{zadatak.zadid}_{tim.nazivtima}.zip'
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{naziv_fajla}"'
    return response


@role_required(ASISTENT)
def ocenjivanje_resenja(request, tim_id, zad_id):
    """
    Funkcija koja se sastoji iz GET dela koji samo prikazuje formu za ocenjivanje asistentu i POST
    dela koji azurira bazu podataka, tako sto ili kreira novi red u tabeli Ocena ukoliko taj zadatak pre nije ocenjen
    ili u istom redu upisuje nove parametre ocene
    """

    ocena = Ocena.objects.filter(timid=tim_id, zadid=zad_id).first()

    if request.method == 'POST':
        form = OceniZadatakForma(request.POST, instance=ocena)
        if form.is_valid():
            tim = Tim.objects.filter(timid=tim_id).first()
            zadatak = Zadatak.objects.filter(zadid=zad_id).first()
            asistent = Asistent.objects.filter(korid=request.user).first()
            nova_ocena = form.save(commit=False)
            nova_ocena.timid = tim
            nova_ocena.zadid = zadatak
            nova_ocena.korid = asistent
            nova_ocena.save()
            novo_obavestenje = Obavestenje.objects.create(naslov="Zadatak ocenjen", tekst=f"Vaša ocena je: {nova_ocena.bodovi} od 100", korid=request.user)
            clanovi = UTimu.objects.filter(timid=tim_id)
            for clan in clanovi:
                Primio.objects.create(korid = clan.korid.korid, obid = novo_obavestenje)
            return redirect('asistent:tabela_resenja', zad_id=zadatak.zadid)
    else:
        form = OceniZadatakForma(instance=ocena)
    return render(request, 'app/asistent/ocenjivanje_resenja.html', {'form': form})