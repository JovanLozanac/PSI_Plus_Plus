import csv
import io

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, IntegrityError
from django.views.decorators.http import require_http_methods

from app.forms.admin import KreiranjeKorisnikaForma, KreiranjeStudentaForma, KreiranjeGrupeStudenataForma
from app.models import Korisnik, Admin, Asistent, Student, UTimu, Tim, Zahteva, Projekat, Primio, Obavestenje
from app.permissions import role_required, ADMIN

#Autor Artjom Uljanov 2023/0421

@role_required(ADMIN)
def admin_glavna(request):
    """
    Glavna stranica za admina
    """
    korisnici = Korisnik.objects.select_related('admin', 'asistent', 'student').all()
    context = {'korisnici': korisnici}
    return render(request, 'app/admin/glavna.html', context)


@role_required(ADMIN)
@require_http_methods(["DELETE"])
def obrisi_korisnika(request, korid):
    """
    View koji brise korisnika sa specificiranim ID-jem. Dozvoljen je samo ADMIN korisnicima.
    Prima samo DELETE metodu i vraca JsonResponse. Namenjen je za koriscenje preko AJAX-a.
    """
    korisnik = get_object_or_404(
        Korisnik.objects.select_related('admin', 'asistent', 'student'),
        korid=korid,
    )

    if korisnik.korid == request.user.korid:
        return JsonResponse({'error': 'Ne možete obrisati sopstveni nalog.'}, status=400)

    try:
        with transaction.atomic():
            if korisnik.je_admin:
                korisnik.admin.delete()
            elif korisnik.je_asistent:
                korisnik.asistent.delete()
            elif korisnik.je_student:
                korisnik.student.delete()
            korisnik.delete()
    except IntegrityError:
        return JsonResponse(
            {'error': 'Korisnik ne može biti obrisan zbog povezanih podataka.'},
            status=409,
        )

    return JsonResponse({'success': True, 'korid': korid})


@role_required(ADMIN)
def brisanje_svih_studenata(request):
    """
    View koji brise sve studente i sve povezane podatke (zahteve, timove, projekte, obavestenja i sl.).
    Dozvoljen je samo ADMIN korisnicima. Prima GET i POST metodu; u slucaju uspeha preusmerava
    na glavnu stranicu, a u slucaju greske (IntegrityError) vraca potvrdnu formu sa porukom o gresci.
    Brisanje se izvrsava unutar transakcije kako bi se izbeglo delimicno brisanje podataka.
    """
    if request.method == "POST":
        try:
            with transaction.atomic():
                student_korisnici_ids = list(
                    Korisnik.objects.filter(student__isnull=False).values_list('korid', flat=True)
                )
                Zahteva.objects.all().delete()
                UTimu.objects.all().delete()
                Projekat.objects.all().delete()
                Tim.objects.all().delete()
                Primio.objects.filter(korid_id__in=student_korisnici_ids).delete()
                Obavestenje.objects.filter(korid_id__in=student_korisnici_ids).delete()
                Student.objects.all().delete()
                Korisnik.objects.filter(korid__in=student_korisnici_ids).delete()
        except IntegrityError:
            return render(request, 'app/admin/brisanje_potvrda.html', {
                'greska': 'Brisanje studenata nije uspelo zbog povezanih podataka.',
            })
        return redirect('upravljanje:glavna')

    return render(request, 'app/admin/brisanje_potvrda.html')


@role_required(ADMIN)
def registracija_korisnika(request):
    """
    View koji registruje novog korisnika i kreira odgovarajuci povezani zapis (Admin, Asistent ili Student)
    u zavisnosti od izabrane uloge. Prima GET i POST metodu; kod GET-a prikazuje praznu formu (podrazumevana uloga
    je "student"), a kod POST-a validira unete podatke i, ako su ispravni, cuva korisnika unutar transakcije.
    U slucaju neuspesne validacije, ponovo prikazuje formu sa unetim vrednostima i izabranom ulogom.
    """
    if request.method == "POST":
        uloga = request.POST.get("uloga")

        korisnik_forma = KreiranjeKorisnikaForma(request.POST)
        student_forma = KreiranjeStudentaForma(request.POST) if uloga == "student" else KreiranjeStudentaForma()

        if korisnik_forma.is_valid() and (uloga != "student" or student_forma.is_valid()):
            with transaction.atomic():
                korisnik = korisnik_forma.save()
                match uloga:
                    case "admin":
                        Admin.objects.create(korid=korisnik)
                    case "asistent":
                        Asistent.objects.create(korid=korisnik)
                    case "student":
                        student = student_forma.save(commit=False)
                        student.korid = korisnik
                        student.jekapiten = 0
                        student.save()
            return redirect("upravljanje:glavna")

        izabrana_uloga = uloga
    else:
        izabrana_uloga = "student"
        korisnik_forma = KreiranjeKorisnikaForma()
        student_forma = KreiranjeStudentaForma()

    return render(request, "app/admin/registracija.html", {
        "korisnik_forma": korisnik_forma,
        "student_forma": student_forma,
        "izabrana_uloga": izabrana_uloga,
    })

NAZIVI_POLJA = {
    "username": "korisničko ime",
    "email": "email",
    "first_name": "ime",
    "last_name": "prezime",
    "password": "lozinka",
    "indeks": "indeks",
    "__all__": "opšta greška",
}


def formatiraj_gresku(e: ValidationError) -> str:
    """
    Formatira Django ValidationError u oblik prikladan za prikazivanje korisniku.
    """
    if hasattr(e, "message_dict"):
        delovi = []
        for polje, poruke in e.message_dict.items():
            naziv = NAZIVI_POLJA.get(polje, polje)
            delovi.append(f"{naziv}: {' '.join(poruke)}")
        return "; ".join(delovi)
    return " ".join(e.messages)


@role_required(ADMIN)
def registracija_grupe_studenata(request):
    """
    View koji registruje vise studenata odjednom na osnovu CSV fajla.
    Prima GET i POST metodu; kod POST-a proverava da li je fajl u UTF-8 kodiranju i da li sadrzi sve obavezne kolone
    (korisnicko_ime, email, ime, prezime, lozinka, indeks), a zatim za svaki red kreira odgovarajuceg Korisnika i Studenta unutar transakcije.
    Ako dodje do greske (nevalidni podaci, dupliranje korisnickog imena/indeksa ili nedostajuca kolona),
    cela transakcija se ponistava i formi se dodaje poruka o gresci sa naznakom reda u kom je greska nastala.
    """
    if request.method == "POST":
        forma = KreiranjeGrupeStudenataForma(request.POST, request.FILES)
        if forma.is_valid():
            fajl = forma.cleaned_data["fajl"]

            try:
                decoded = io.TextIOWrapper(fajl.file, encoding="utf-8")
                reader = csv.DictReader(decoded)
            except UnicodeDecodeError:
                forma.add_error("fajl", "Fajl mora biti u UTF-8 kodiranju.")
                return render(request, "app/admin/registracija_grupe_studenata.html", {"form": forma})

            obavezne_kolone = {"korisnicko_ime", "email", "ime", "prezime", "lozinka", "indeks"}
            if not reader.fieldnames or not obavezne_kolone.issubset(set(reader.fieldnames)):
                forma.add_error(
                    "fajl",
                    "CSV fajl mora sadržati kolone: " + ", ".join(sorted(obavezne_kolone)),
                )
                return render(request, "app/admin/registracija_grupe_studenata.html", {"form": forma})

            redovi = list(reader)
            greska = None

            try:
                with transaction.atomic():
                    for broj_reda, red in enumerate(redovi, start=2):  # red 1 je header
                        korisnik = Korisnik(
                            username=red["korisnicko_ime"].strip(),
                            email=red["email"].strip(),
                            first_name=red["ime"].strip(),
                            last_name=red["prezime"].strip(),
                        )
                        korisnik.set_password(red["lozinka"])
                        korisnik.full_clean()
                        korisnik.save()

                        student = Student(
                            korid=korisnik,
                            jekapiten=0,
                            indeks=red["indeks"].strip(),
                        )
                        student.full_clean()
                        student.save()
            except ValidationError as e:
                greska = f"Greška u redu {broj_reda}: {formatiraj_gresku(e)}"
            except IntegrityError:
                greska = f"Greška u redu {broj_reda}: korisničko ime ili indeks se već koristi"
            except (KeyError, AttributeError):
                greska = f"Nedostaje kolona u redu {broj_reda}."

            if greska:
                forma.add_error(None, greska)
            else:
                return redirect("upravljanje:glavna")
    else:
        forma = KreiranjeGrupeStudenataForma()
    return render(request, "app/admin/registracija_grupe_studenata.html", {"form": forma})