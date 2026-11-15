import io
import zipfile

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Prefetch, Count
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from ..models import Student, Tim, UTimu, Zadatak, Zahteva, Ocena, Obavestenje, Primio, Projekat
from pathlib import Path

#Autor Jovan Lozanac 2023/0084
#Autor Luka Milic 2022/0182
#Autor Artjom Uljanov 2023/0421
#Autor David Radivojevic 2021/0504

GLAVNE_STRANICE = {
    "admin": "upravljanje:glavna",
    "asistent": "asistent:glavna",
    "student": "student:glavna",
}

projekti_path = 'projekti'

@login_required
def homepage_dispatcher(request):
    """
    View koji preusmerava korisnika na pocetnu stranicu u zavisnosti od njegove uloge (admin, asistent ili student).
    Ako uloga nije prepoznata (nije definisana u recniku GLAVNE_STRANICE), korisnik se odjavljuje.
    """
    glavna_stranica = GLAVNE_STRANICE.get(request.user.role)
    if glavna_stranica:
        return redirect(glavna_stranica)
    return redirect('odjava')


@login_required
def profil_korisnika(request):
    """
    View za prikazivanje profila korisnika
    """
    return render(request, "app/profil.html")

@login_required
def promena_lozinke(request):
    """
    View za promenu lozinke korisnika. Prima GET i POST metodu; kod GET-a prikazuje praznu formu,
    a kod POST-a validira unete podatke i, ako su ispravni, cuva izmenjenu lozinku.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/promena_lozinke.html', {'form': form})


@login_required
def lista_timova(request):
    """
    View koji prikazuje listu timova i listu studenata koji nisu u timu
    """
    timovi = Tim.objects.annotate(
    br=Count('utimu')
    ).prefetch_related(
        Prefetch(
            'utimu_set',
            queryset=UTimu.objects.select_related('korid__korid')
        )
    )
    nema_tim = Student.objects.exclude(
        pk__in=UTimu.objects.values('korid__korid')
    ).select_related('korid')
    if request.user.je_student:
        timovi_zahtevi = [(tim, Zahteva.objects.filter(timid=tim, korid=request.user.student).exists()) for tim in timovi]
    else:
        timovi_zahtevi = [(tim, False) for tim in timovi]
    return render(request, 'app/lista_timova.html', {'timovi_zahtevi': timovi_zahtevi, 'nema_tim': nema_tim, 'formiranje_timova': Zadatak.formiranje_timova_dozvoljeno()})


@login_required
def prikaz_tima(request, timid):
    """
    View prikazuje tim
    """
    tim = Tim.objects.get(timid=timid)
    kapiten = UTimu.objects.get(timid=tim, korid__jekapiten=1).korid
    clanovi = [student.korid for student in UTimu.objects.filter(timid=tim, korid__jekapiten=0)]
    broj_zahteva = Zahteva.objects.filter(timid=tim).count()
    ocene = Ocena.objects.filter(timid=tim)
    ulogovan_clan_tima = False
    sadrzaj_projekta = dohvati_projekat(timid)

    if request.user.je_student:
        ulogovan_clan_tima = UTimu.objects.filter(timid=tim, korid=request.user.student).exists()
    context = {
        'tim': tim,
        'kapiten': kapiten,
        'clanovi': clanovi,
        'broj_zahteva': broj_zahteva,
        'formiranje_timova_dozvoljeno': Zadatak.formiranje_timova_dozvoljeno(),
        'ocene': ocene,
        'ulogovan_clan_tima': ulogovan_clan_tima,
        'sadrzaj_projekta': sadrzaj_projekta
    }
    return render(request, 'app/tim.html', context)


def dohvati_obavestenja(user):
    """
    Pomocna funkcija za dohvatanje svih obavestenja za jednog korisnika, sortirano od najnovijeg
    """
    return Primio.objects.filter(korid=user.korid).order_by('-obid')


def dohvati_broj_neprocitanih(user):
    """
    Pomocna funkcija koja vraca broj neprocitanih obavestenja
    """
    return Primio.objects.filter(korid=user.korid, procitano=False).count()


def dohvati_projekat(timid, zadatak_id = None):
    """
    Pomocna funkcija koja dohvata sadrzaj projekta i vraca njegov sadrzaj, koriscenja je za prikaz projekta i
    studentu i asistentu, u zavisnosti od argumenata funkcije
    """
    if zadatak_id:
        p = f'projekti/zadatak_{zadatak_id}/tim_{timid}'
    else:
        p = f'projekti/latest/tim_{timid}'

    path = Path(p)

    projekat = Projekat.objects.filter(folder=p).first()
    if projekat:
        vreme = projekat.updatum
    else:
        vreme = None

    # Deo za ulazak direktno u bitne fajlove, jer obicno zipovan folder ima obican folder u kome se nalaze prave stvari
    if path.exists() and path.is_dir():
        sve_stavke = list(path.iterdir())
        if len(sve_stavke) == 1 and sve_stavke[0].is_dir():
            path = sve_stavke[0]

    sadrzaj = []

    if path.exists() and path.is_dir():
        for stavka in path.iterdir():
            sadrzaj.append({
                'ime': stavka.name,
                'je_folder': stavka.is_dir(),
                'vreme': vreme,
                'putanja': str(stavka)
            })

    sadrzaj.sort(key=lambda x: (not x['je_folder'], x['ime'].lower()))

    return sadrzaj


@login_required
def prikaz_obavestenja(request):
    """
    Preusmerava korisnika na stranicu za prikaz obavestenja
    """
    obavestenja = dohvati_obavestenja(request.user)

    Primio.objects.filter(korid=request.user.korid, procitano=False).update(procitano=True)

    context = {'obavestenja': obavestenja}

    return render(request, "app/prikaz_obavestenja.html", context)



def dohvati_poddirektorijum(putanja, timid):
    """
    Pomocna funkcija koja sluzi za dohvatanje direktorijuma sa prosledjenom putanjom, koriscena je za implementaciju file explorera
    """
    path = Path(putanja)

    projekat = Projekat.objects.filter(timid=timid).first()
    vreme = projekat.updatum if projekat else None

    sadrzaj = []

    if path.exists() and path.is_dir():
        for stavka in path.iterdir():
            sadrzaj.append({
                'ime': stavka.name,
                'je_folder': stavka.is_dir(),
                'vreme': vreme,
                'putanja': str(stavka)  # Ključno: pakuje punu putanju za sledeći klik!
            })

    sadrzaj.sort(key=lambda x: (not x['je_folder'], x['ime'].lower()))

    return sadrzaj


@login_required
def prikaz_direktorijuma(request, timid):
    """
    Funkcija koja prikazuje strukturu konkretnog direktorijuma, izlistavajuci sav njegov sadrzaj
    """
    tim = Tim.objects.get(timid=timid)

    trenutna_putanja = request.GET.get('putanja', '')

    sadrzaj_direktorijuma = dohvati_poddirektorijum(trenutna_putanja, tim.timid)

    roditelj = str(Path(trenutna_putanja).parent)

    context = {
        'tim': tim,
        'sadrzaj_direktorijuma': sadrzaj_direktorijuma,
        'trenutna_putanja': trenutna_putanja,
        'roditelj_putanja': roditelj,
        'ime_trenutnog_foldera': Path(trenutna_putanja).name
    }
    return render(request, 'app/prikaz_direktorijuma.html', context)


@login_required
def prikaz_fajla(request, timid):
    """
    Funkcija koja preusmerava korisnika na stranicu sa prikazom teksta konkretnog fajla
    """
    tim = Tim.objects.get(timid=timid)
    putanja_fajla = request.GET.get('putanja', '')
    path = Path(putanja_fajla)

    sadrzaj_koda = ""

    if path.exists() and path.is_file():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                sadrzaj_koda = f.read()
        except Exception:
            sadrzaj_koda = "Greška prilikom čitanja fajla. Moguće je da je fajl binaran ili ima neispravan encoding."

    context = {
        'tim': tim,
        'ime_fajla': path.name,
        'kod': sadrzaj_koda,
    }
    return render(request, 'app/prikaz_fajla.html', context)

@login_required
def preuzimanje_projekta(request, timid):
    """
    Zipuje projekat tima iz foldera projekti/latest/tim_<timid>
    i vraca ga korisniku na preuzimanje.
    """
    tim = Tim.objects.get(timid=timid)
    folder = f'{projekti_path}/latest/tim_{tim.timid}'
    path = Path(folder)
    if not path.exists() or not Projekat.objects.filter(folder=folder).exists():
        raise Http404('Projekat nije pronađen.')

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in path.rglob('*'):
            if file_path.is_file():
                zip_file.write(file_path, file_path.relative_to(path))
    buffer.seek(0)

    naziv_fajla = f'{tim.nazivtima}_latest.zip'
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{naziv_fajla}"'
    return response