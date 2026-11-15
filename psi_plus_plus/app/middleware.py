import random

from django.utils import timezone

from django.db import transaction

from app.models import Korisnik, Student, UTimu, Tim, Zadatak, Zahteva
#Autor Jovan Lozanac 2023/0084
#Autor Luka Milic 2022/0182
#Autor Artjom Uljanov 2023/0421

class AttachRoleMiddleware:
    """
    Izvršava se nakon AuthenticationMiddleware. Zamenjuje request.user
    verzijom koja ima admin/asistent/student unapred učitane (prefetch) preko
    select_related, tako da ništa dalje niz lanac (view-ovi, context processor-i,
    template-i) ne mora ponovo da pogađa bazu da bi proverilo ulogu korisnika.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = (
                Korisnik.objects
                .select_related('admin', 'asistent', 'student')
                .get(pk=request.user.pk)
            )
        return self.get_response(request)

class AssignTeamsMiddleware:
    """
    Izvršava se nakon AttachRoleMiddleware. Ubacuje se u request korisnika i osvežava DB
    (prilikom osvežavanja stranice) pod uslovom da je prošao rok
    nulte faze a postoje studenti koji nisu u timu. Takođe u ove studente uvrštava i
    studente u jednočlanom timu, i briše im timove. Koristeći algoritme razdvajanja brojeva na sabirke,
    pravi nasumične sastave timova, favorizujući timove od 3 i 4 člana.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with transaction.atomic():
            if Zadatak.formiranje_timova_dozvoljeno(): return self.get_response(request)
            else: Zahteva.objects.all().delete()
            zadatak = (
                Zadatak.objects
                .select_for_update()
                .filter(
                    brfaze=0,
                    rok__lte=timezone.now(),
                )
                .order_by('-rok')
                .first()
            )
            if zadatak:
                jednoclani_timovi = [tim for tim in Tim.objects.all() if tim.br_clanova == 1]

                for tim in jednoclani_timovi:
                    UTimu.objects.filter(timid=tim).delete()
                    tim.delete()

                bez_tima = list(
                    Student.objects.filter(
                        utimu__isnull=True
                    )
                )

                if not bez_tima:
                    return self.get_response(request)

                if len(bez_tima) == 1:
                    student = bez_tima[0]
                    timovi = list(Tim.objects.all())
                    min_br_clanova = min(tim.br_clanova for tim in timovi)
                    timovi = [tim for tim in timovi if tim.br_clanova == min_br_clanova]
                    tim = random.choice(timovi)
                    UTimu.objects.create(korid=student, timid=tim)
                    student.jekapiten = 0
                    student.save()
                    return self.get_response(request)

                random.shuffle(bez_tima)

                for i in range(len(bez_tima)):
                    student = bez_tima[i]
                    if i % 4 == 0:
                        student.jekapiten = 1
                    else:
                        student.jekapiten = 0
                    student.save()

                novi_timovi = []
                while len(bez_tima) > 0:
                    n = len(bez_tima)
                    if n == 2:
                        novi_timovi.append(bez_tima[:2])
                        break
                    elif n == 3:
                        novi_timovi.append(bez_tima[:3])
                        break
                    elif n == 5 or n == 6:
                        novi_timovi.append(bez_tima[:3])
                        novi_timovi.append(bez_tima[3:])
                        break
                    else:
                        novi_timovi.append(bez_tima[:4])
                        bez_tima = bez_tima[4:]

                for nt in novi_timovi:
                    if Tim.objects.all().exists():
                        novi_id = Tim.objects.all().values_list('timid', flat=True).order_by('-timid').first() + 1
                    else:
                        novi_id = 1
                    novi_tim = Tim.objects.create(
                        timid=novi_id,
                        nazivtima=f"Tim {novi_id}"
                    )

                    UTimu.objects.bulk_create([
                        UTimu(
                            korid=s,
                            timid=novi_tim
                        )
                        for s in nt
                    ])

        return self.get_response(request)