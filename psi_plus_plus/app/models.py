from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

#Autor Luka Milic 2022/0182
#Autor Artjom Uljanov 2023/0421
#Autor David Radivojevic 2021/0504

class Admin(models.Model):
    """
    Model admina
    korid - int: strani kljuc korisnika
    """
    korid = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='KorID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'admin'


class Asistent(models.Model):
    """
    Model asistenta
    korid - int: strani kljuc korisnika
    """
    korid = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='KorID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'asistent'


class Korisnik(AbstractUser):
    """
    Model korisnika
    korid - int: primarni kljuc
    """
    korid = models.AutoField(db_column='KorID', primary_key=True)  # Field name made lowercase.

    def __str__(self):
        """
        Vraca string reprezentaciju korisnika
        """
        return f"{self.first_name} {self.last_name} (ID={str(self.korid)})"

    @property
    def role(self):
        """
        Vraca string reprezentaciju role korisnika
        """
        if hasattr(self, 'admin'):
            return 'admin'
        if hasattr(self, 'asistent'):
            return 'asistent'
        if hasattr(self, 'student'):
            return 'student'
        return None

    @property
    def je_admin(self):
        """
        Vraca True ako je korisnik admin, False u suprotnom
        """
        return hasattr(self, 'admin')

    @property
    def je_asistent(self):
        """
        Vraca True ako je korisnik asistent, False u suprotnom
        """
        return hasattr(self, 'asistent')

    @property
    def je_student(self):
        """
        Vraca True ako je korisnik student, False u suprotnom
        """
        return hasattr(self, 'student')

    class Meta:
        db_table = 'korisnik'


class Obavestenje(models.Model):
    """
    Model obavestenja
    obid - int: primarni kljuc
    naslov - string: naslov obavestenja
    tekst - string: tekst obavestenja
    korid - int: strani kljuc korisnika koji je poslao obavestenje
    """
    obid = models.AutoField(db_column='ObID', primary_key=True)  # Field name made lowercase.
    naslov = models.CharField(db_column='Naslov', max_length=100)  # Field name made lowercase.
    tekst = models.CharField(db_column='Tekst', max_length=300)  # Field name made lowercase.
    korid = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='KorID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'obavestenje'


class Ocena(models.Model):
    """
    Model ocene koju asistent daje zadatku
    ocid - int: primarni kljuc
    zadid - int: strani kljuc ocenjenog zadatka
    timid - int: strani kljuc ocenjenog tima
    korid - int: strani kljuc asistenta koji je dao ocenu
    bodovi - float(-100, 100): bodovi sa kojima je asistent bodovao zadatak
    komentar - string: utisak koji asistent dodaje uz ocenu
    """
    ocid = models.AutoField(db_column='OcID', primary_key=True)  # Field name made lowercase.
    zadid = models.ForeignKey('Zadatak', models.DO_NOTHING, db_column='ZadID')  # Field name made lowercase.
    timid = models.ForeignKey('Tim', models.DO_NOTHING, db_column='TimID')  # Field name made lowercase.
    korid = models.ForeignKey(Asistent, models.DO_NOTHING, db_column='KorID')  # Field name made lowercase.
    bodovi = models.DecimalField(db_column='Bodovi', max_digits=4, decimal_places=2)  # Field name made lowercase.
    komentar = models.CharField(db_column='Komentar', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'ocena'


class Primio(models.Model):
    """
    Model koji povezuje obavestenje sa korisnikom koji ga je dobio
    pk: Kompozitni primarni kljuc -> korid + obid
    korid - int: strani kljuc korisnika koji je primio obavestenje
    obid - int: strani kljuc obavestenja
    procitano - bool: indikator koji kaze da li je korisnik video obavestenje
    """
    pk = models.CompositePrimaryKey('korid', 'obid')
    korid = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='KorID')  # Field name made lowercase.
    obid = models.ForeignKey(Obavestenje, models.DO_NOTHING, db_column='ObID')  # Field name made lowercase.
    procitano = models.BooleanField(default=False)

    class Meta:
        db_table = 'primio'


class Projekat(models.Model):
    """
    Model predatog projekta
    prid - int: primarni kljuc
    folder - string: putanja do foldera u kojem se sadrzi predani projekat
    updatum - datetime: datum i vreme predaje projekta
    timid - int: strani kljuc tima koji je predao projekat
    """
    prid = models.AutoField(db_column='PrID', primary_key=True)  # Field name made lowercase.
    folder = models.CharField(db_column='Folder', max_length=100)  # Field name made lowercase.
    updatum = models.DateTimeField(db_column='UpDatum')  # Field name made lowercase.
    timid = models.ForeignKey('Tim', models.DO_NOTHING, db_column='TimID')  # Field name made lowercase.

    class Meta:
        db_table = 'projekat'


indeks_validator = RegexValidator(
    regex=r"^\d{4}/\d{4}$",
    message="Indeks mora biti u formatu GGGG/BBBB (npr. 2023/0111).",
    code="invalid_indeks",
)


class Student(models.Model):
    """
    Model studenta
    korid - int: strani kljuc korisnika
    jekapiten - int: indikator da li je student kapiten tima u kome se nalazi
    indeks - string: indeks studenta
    """
    korid = models.OneToOneField(Korisnik, models.DO_NOTHING, db_column='KorID', primary_key=True)  # Field name made lowercase.
    jekapiten = models.IntegerField(db_column='JeKapiten', blank=True, null=True)  # Field name made lowercase.
    indeks = models.CharField(
        db_column='Indeks',
        unique=True,
        max_length=9,
        validators=[indeks_validator],
    )  # Field name made lowercase.

    def __str__(self):
        """
        Vraca string reprezentaciju studenta
        """
        return self.indeks

    @property
    def trenutno_u_timu(self):
        """
        Vraca True ako je student u timu, False u suprotnom
        """
        return UTimu.objects.filter(korid=self).exists()

    @property
    def tim(self):
        """
        Vraca tim u kom se student nalazi, ako student nije u timu vraca None
        """
        if not self.trenutno_u_timu:
            return None
        return UTimu.objects.get(korid=self).timid

    class Meta:
        db_table = 'student'


class Tim(models.Model):
    """
    Model tima
    timid - int: primarni kljuc
    nazivtima - string: naziv tima
    imeprojekta - string: ime projekta
    opisprojekta - string: opis projekta
    """
    timid = models.AutoField(db_column='TimID', primary_key=True)  # Field name made lowercase.
    nazivtima = models.CharField(db_column='NazivTima', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    imeprojekta = models.CharField(db_column='ImeProjekta', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    opisprojekta = models.CharField(db_column='OpisProjekta', max_length=300, blank=True, null=True)  # Field name made lowercase.

    @property
    def br_clanova(self):
        """
        Vraca broj studenata u timu
        """
        return UTimu.objects.filter(timid=self).count()

    class Meta:
        db_table = 'tim'


class UTimu(models.Model):
    """
    Model veze tima i studenta
    korid - int: primarni kljuc i strani kljuc studenta iz nekog tima
    timid - int: strani kljuc tima kome student pripada
    """
    korid = models.OneToOneField(Student, models.DO_NOTHING, db_column='KorID', primary_key=True)  # Field name made lowercase.
    timid = models.ForeignKey(Tim, models.DO_NOTHING, db_column='TimID')  # Field name made lowercase.

    class Meta:
        db_table = 'u_timu'


class Zadatak(models.Model):
    """
    Model zadatka koji pravi asistent
    zadid - int: primarni kljuc
    rok - datetime: krajnji rok predaje zadatka
    naslov - string: naslov zadatka
    tekst - string: tekst zadatka
    brfaze - int: redni broj faze (ako je 0 zadatak oznacava formiranje timova)
    korid - int: strani kljuc asistenta koji je napravio zadatak
    """
    zadid = models.AutoField(db_column='ZadID', primary_key=True)  # Field name made lowercase.
    rok = models.DateTimeField(db_column='Rok')  # Field name made lowercase.
    naslov = models.CharField(db_column='Naslov', max_length=45)  # Field name made lowercase.
    tekst = models.CharField(db_column='Tekst', max_length=300)  # Field name made lowercase.
    brfaze = models.IntegerField(db_column='BrFaze')  # Field name made lowercase.
    korid = models.ForeignKey(Asistent, models.DO_NOTHING, db_column='KorID')  # Field name made lowercase.

    @property
    def je_formiranje_timova(self):
        """
        Vraca True ako je u pitanju formiranje timova, False u suprotnom
        """
        return self.brfaze == 0

    @property
    def u_toku(self):
        """
        Vraca True ako zadatku nije istekao rok, False u suprotnom
        """
        return self.rok > timezone.now()

    @staticmethod
    def formiranje_timova_dozvoljeno():
        """
        Vraca True ako je formiranje timova u toku, False ako je suprotno
        """
        return Zadatak.objects.filter(brfaze=0, rok__gt=timezone.now()).exists()

    class Meta:
        db_table = 'zadatak'


class Zahteva(models.Model):
    """
    Model koji predstavlje zahtev studenta da se uclani u tim
    pk: kompozitni primarni kljuc -> korid + timid
    korid - int: strani kljuc studenta koji je poslao zahtev
    timid - int: strani kljuc tima u koji student zahteva da se uclani
    """
    pk = models.CompositePrimaryKey('korid', 'timid')
    korid = models.ForeignKey(Student, models.DO_NOTHING, db_column='KorID')  # Field name made lowercase.
    timid = models.ForeignKey(Tim, models.DO_NOTHING, db_column='TimID')  # Field name made lowercase.

    class Meta:
        db_table = 'zahteva'