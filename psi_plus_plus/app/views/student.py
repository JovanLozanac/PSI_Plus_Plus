from django.shortcuts import render, redirect
from django.utils import timezone
from django.db import transaction

from app.permissions import role_required, STUDENT
from app.models import Zadatak, Tim, Zahteva, UTimu, Obavestenje, Primio, Korisnik, Projekat
from app.forms.student import TimForma, UpdateTimForma
from app.views.common import projekti_path

import zipfile
from pathlib import Path
import shutil
#Autor Luka Milic 2022/0182

@role_required(STUDENT)
def student_glavna(request):
    """
    View na glavnu stranicu za studenta
    """
    zadaci = Zadatak.objects.filter(rok__gt=timezone.now())
    tim = None
    if request.user.student.trenutno_u_timu:
        tim = request.user.student.tim
    context = {
        'zadaci': zadaci,
        'tim': tim
    }
    return render(request, 'app/student/glavna.html', context)


@role_required(STUDENT)
def zahtev_poslat(request):
    """
    View koji salje zahtev i potvrdjuje korisniku da je zahtev poslat
    """
    timid = request.POST.get('timid')
    tim = Tim.objects.get(timid=timid)
    if Zahteva.objects.filter(korid=request.user.student, timid=tim):
        return render(request, 'app/student/zahtev_poslat.html', {'poruka': 'Već ste poslali zahtev ovom timu.'})
    with transaction.atomic():
        Zahteva.objects.create(korid=request.user.student, timid=tim)
        naslov_obavestenja = 'Zahtev za učlanjenje'
        tekst_obavestenja = f'Student {request.user.first_name} {request.user.last_name} želi da bude deo vašeg tima.'
        obavestenje = Obavestenje.objects.create(naslov=naslov_obavestenja, tekst=tekst_obavestenja, korid=request.user)
        kapiten = UTimu.objects.filter(timid=tim, korid__jekapiten=1).first().korid
        Primio.objects.create(korid=kapiten.korid, obid=obavestenje)
    return render(request, 'app/student/zahtev_poslat.html', {'poruka': 'Zahtev za pridruživanje timu je poslat. Čekajte na odobrenje.'})


@role_required(STUDENT)
def pravljenje_tima(request):
    """
    View prikazuje formu za pravljenje tima ako je GET metoda,
    ako je POST pravi odgovarajuci tim
    """
    if request.method == 'POST':
        form = TimForma(request.POST)
        if form.is_valid():
            naziv_tima = form.cleaned_data['nazivtima']
            with transaction.atomic():
                tim = Tim.objects.create(nazivtima=naziv_tima)
                request.user.student.jekapiten = 1
                request.user.student.save()
                UTimu.objects.create(korid=request.user.student, timid=tim)
                Zahteva.objects.filter(korid=request.user.student).delete()
                for folder in Path(projekti_path).iterdir():
                    if folder.is_dir():
                        new_folder = folder / f'tim_{tim.timid}'
                        new_folder.mkdir(exist_ok=True)
            return redirect('student:glavna')
        else:
            return render(request, 'app/student/pravljenje_tima.html', {'form': TimForma(), 'poruka': 'Tim sa tim imenom već postoji.'})
    return render(request, 'app/student/pravljenje_tima.html', {'form': TimForma(), 'poruka': ''})


@role_required(STUDENT)
def azuriranje_tima(request):
    """
    Ako je request.method == 'GET' view vraca stranicu za promenu podatak tima.
    Ako je request.method == 'POST' view cuva promene u bazi.
    """
    tim = request.user.student.tim
    form = UpdateTimForma(initial={
        'nazivtima': tim.nazivtima,
        'imeprojekta': tim.imeprojekta,
        'opisprojekta': tim.opisprojekta
    })
    if request.method == 'POST':
        form = UpdateTimForma(request.POST)
        if form.is_valid():
            naziv_tima = form.cleaned_data['nazivtima']
            ime_projekta = form.cleaned_data['imeprojekta']
            opis_projekta = form.cleaned_data['opisprojekta']
            naziv_vec_postoji = Tim.objects.exclude(timid=tim.timid).filter(nazivtima=naziv_tima).exists()
            ime_projekta_vec_postoji = Tim.objects.exclude(timid=tim.timid).filter(imeprojekta=ime_projekta).exists()
            if naziv_vec_postoji:
                return render(request, 'app/student/azuriranje_tima.html',
                              {'form': form, 'poruka': 'Tim sa tim imenom već postoji.'})
            elif ime_projekta_vec_postoji:
                return render(request, 'app/student/azuriranje_tima.html',
                              {'form': form, 'poruka': 'Tim sa tim imenom projekta već postoji.'})
            with transaction.atomic():
                tim.nazivtima = naziv_tima
                tim.imeprojekta = ime_projekta
                tim.opisprojekta = opis_projekta
                tim.save()
            return redirect('prikaz_tima', timid=tim.timid)
    return render(request, 'app/student/azuriranje_tima.html', {'form': form, 'poruka': ''})


@role_required(STUDENT)
def prikaz_zahteva(request):
    """
    Prikazuje stranicu sa listom zahteva.
    """
    tim = request.user.student.tim
    zahtevi = Zahteva.objects.filter(timid=tim)
    return render(request, 'app/student/prikaz_zahteva.html', {'zahtevi': zahtevi})


@role_required(STUDENT)
def obrada_zahteva(request, korid):
    """
    Obradjuje prihvatanje ili odbijanje zahteva.
    """
    student = Korisnik.objects.get(korid=korid).student
    prihvacen = int(request.POST.get('prihvacen'))
    tim = request.user.student.tim
    if prihvacen == 1:
        with transaction.atomic():
            UTimu.objects.create(timid=tim, korid=student)
            Zahteva.objects.filter(korid=student).delete()
            obavestenje = Obavestenje.objects.create(
                naslov='Zahtev je prihvacen',
                tekst=f'Kapiten tima {tim.nazivtima} je prihvatio vaš zahtev za članstvo.',
                korid=request.user.student.korid
            )
            Primio.objects.create(korid=student.korid, obid=obavestenje)
    else:
        with transaction.atomic():
            Zahteva.objects.get(korid=student, timid=tim).delete()
            obavestenje = Obavestenje.objects.create(
                naslov='Zahtev je odbijen',
                tekst=f'Kapiten tima {tim.nazivtima} je odbio vaš zahtev za članstvo.',
                korid=request.user.student.korid
            )
            Primio.objects.create(korid=student.korid, obid=obavestenje)
    return redirect('prikaz_tima', timid=request.user.student.tim.timid)


@role_required(STUDENT)
def cuvanje_projekta(request):
    """
    Cuva projekat koji student uploaduje.
    """
    file = request.FILES.get('file')
    tim = request.user.student.tim
    zadaci = Zadatak.objects.filter(rok__gt=timezone.now()).exclude(brfaze=0)
    folders = [f'{projekti_path}/zadatak_{zadatak.zadid}/tim_{tim.timid}' for zadatak in zadaci]
    folders.append(f'{projekti_path}/latest/tim_{tim.timid}')
    with transaction.atomic():
        for folder in folders:
            path = Path(folder)
            if Projekat.objects.filter(folder=folder).exists():
                for item in path.iterdir():
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                projekat = Projekat.objects.get(folder=folder)
                projekat.updatum = timezone.now()
                projekat.save()
            else:
                Projekat.objects.create(folder=folder, updatum=timezone.now(), timid=tim)
            with zipfile.ZipFile(file) as f:
                f.extractall(path)
    return redirect('prikaz_tima', tim.timid)

