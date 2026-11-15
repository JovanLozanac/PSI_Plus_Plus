import io
import tempfile
import time
import zipfile
from pathlib import Path
import shutil


from django.contrib.auth.hashers import check_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import json
from datetime import timedelta, timezone
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from app.middleware import AssignTeamsMiddleware
from app.models import Korisnik, Student, Asistent, Admin, Zadatak, Tim, UTimu, Ocena, Obavestenje, Projekat, Primio, Zahteva
from app.views.common import projekti_path

# Create your tests here.

common_path = 'app'
admin_path = 'app/admin'
asistent_path = 'app/asistent'
student_path = 'app/student'


def create_student(username, indeks):
    korisnik = Korisnik.objects.create(username=username)
    korisnik.set_password('ab1234cd')
    korisnik.save()
    return Student.objects.create(korid=korisnik, indeks=indeks)


def create_asistent(username):
    korisnik = Korisnik.objects.create(username=username)
    korisnik.set_password('ab1234cd')
    korisnik.save()
    return Asistent.objects.create(korid=korisnik)


def create_admin(username):
    korisnik = Korisnik.objects.create(username=username)
    korisnik.set_password('ab1234cd')
    korisnik.save()
    return Admin.objects.create(korid=korisnik)


class BaseSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def login(self, username, homepage):
        self.driver.get(f'{self.live_server_url}/prijava')

        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys('ab1234cd')
        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        WebDriverWait(self.driver, 10).until(
            EC.url_contains(homepage)
        )


class TestLoggedOutTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.korisnik = Korisnik.objects.create(username='TestKorisnik')
        self.korisnik.set_password('12abcd34')
        self.korisnik.save()

    def tearDown(self):
        self.client.post(reverse('odjava'))

    def test_login_form_GET(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/prijava.html')

    def test_login_form_admin_POST(self):
        Admin.objects.create(korid=self.korisnik)
        response = self.client.post(reverse('prijava'), follow=True, data={
            'username': 'TestKorisnik',
            'password': '12abcd34'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')

    def test_login_form_asistent_POST(self):
        Asistent.objects.create(korid=self.korisnik)
        response = self.client.post(reverse('prijava'), follow=True, data={
            'username': 'TestKorisnik',
            'password': '12abcd34'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/glavna.html')

    def test_login_form_student_POST(self):
        Student.objects.create(korid=self.korisnik)
        response = self.client.post(reverse('prijava'), follow=True, data={
            'username': 'TestKorisnik',
            'password': '12abcd34'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{student_path}/glavna.html')

    def test_login_form_fail_POST(self):
        Admin.objects.create(korid=self.korisnik)
        response = self.client.post(reverse('prijava'), follow=True, data={
            'username': 'wrong',
            'password': 'data'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/prijava.html')


class TestLoggedInAdminTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        korisnik = Korisnik.objects.create(username='TestKorisnik')
        korisnik.set_password('12abcd34')
        korisnik.save()
        Admin.objects.create(korid=korisnik)
        self.client.post(reverse('prijava'), data={
            'username': 'TestKorisnik',
            'password': '12abcd34'
        })

    def tearDown(self):
        self.client.get(reverse('odjava'))

    def test_glavna_GET(self):
        asistent = Korisnik.objects.create_user(username='asistent',
                                                password='12abcd34')
        student = Korisnik.objects.create_user(username='student',
                                               password='12abcd34')
        Asistent.objects.create(korid=asistent)
        Student.objects.create(korid=student,
                               jekapiten=0,
                               indeks='2022/0182')
        response = self.client.get(reverse('homepage'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        self.assertContains(response, 'TestKorisnik')
        self.assertContains(response, 'asistent')
        self.assertContains(response, 'student')

    def test_registracija_korisnika_GET(self):
        response = self.client.get(reverse('upravljanje:registracija_korisnika'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(f'{admin_path}/registracija.html')

    def test_registracija_admina_POST(self):
        response = self.client.post(reverse('upravljanje:registracija_korisnika'), follow=True, data={
            'uloga': 'admin',
            'username': 'pera',
            'email': 'nekimejl@gmail.com',
            'first_name': 'Pera',
            'last_name': 'Peric',
            'password1': '12abcd34',
            'password2': '12abcd34'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        korisnici = Korisnik.objects.filter(username='pera')
        self.assertTrue(korisnici.exists())
        self.assertTrue(korisnici.first().je_admin)

    def test_registracija_asistenta_POST(self):
        response = self.client.post(reverse('upravljanje:registracija_korisnika'), follow=True, data={
            'uloga': 'asistent',
            'username': 'pera',
            'email': 'nekimejl@gmail.com',
            'first_name': 'Pera',
            'last_name': 'Peric',
            'password1': '12abcd34',
            'password2': '12abcd34'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        korisnici = Korisnik.objects.filter(username='pera')
        self.assertTrue(korisnici.exists())
        self.assertTrue(korisnici.first().je_asistent)

    def test_registracija_studenta_POST(self):
        response = self.client.post(reverse('upravljanje:registracija_korisnika'), follow=True, data={
            'uloga': 'student',
            'username': 'pera',
            'email': 'nekimejl@gmail.com',
            'first_name': 'Pera',
            'last_name': 'Peric',
            'password1': '12abcd34',
            'password2': '12abcd34',
            'indeks': '2022/0182'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        korisnici = Korisnik.objects.filter(username='pera')
        self.assertTrue(korisnici.exists())
        self.assertTrue(korisnici.first().je_student)

    def registracija_korisnika_fail_POST(self):
        response = self.client.post(reverse('upravljanje:registracija_korisnika'), follow=True, data={
            'uloga': 'admin',
            'username': 'pera',
            'email': 'nekimejl@gmail.com',
            'first_name': 'Pera',
            'last_name': 'Peric',
            'password1': '12abcd34',
            'password2': '12abcd44'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(f'{admin_path}/registracija.html')
        korisnici = Korisnik.objects.filter(username='pera')
        self.assertFalse(korisnici.exists())

    def test_brisanje_korisnika_DELETE(self):
        korisnik = Korisnik.objects.create_user(username='pera',
                                                password='12abcd34')
        Admin.objects.create(korid=korisnik)
        response = self.client.delete(reverse(f'upravljanje:obrisi_korisnika', args=[korisnik.korid]), follow=True)

        self.assertTrue(json.loads(response.content)['success'])
        korisnici = Korisnik.objects.filter(korid=korisnik.korid)
        self.assertFalse(korisnici.exists())
        admini = Admin.objects.filter(korid=korisnik)
        self.assertFalse(admini.exists())

    def test_brisanje_svih_studenata_GET(self):
        response = self.client.get(reverse('upravljanje:brisanje_svih_studenata'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/brisanje_potvrda.html')

    def test_brisanje_svih_studenata_POST(self):
        student1 = Korisnik.objects.create_user(username='pera',
                                                password='12abcd34')
        student2 = Korisnik.objects.create_user(username='marko',
                                                password='12abcd34')
        Student.objects.create(korid=student1,
                               jekapiten=0,
                               indeks='2022/0182')
        Student.objects.create(korid=student2,
                               jekapiten=0,
                               indeks='2022/0183')
        self.assertTrue(Student.objects.all().exists())
        response = self.client.post(reverse('upravljanje:brisanje_svih_studenata'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        self.assertFalse(Student.objects.all().exists())
        self.assertFalse(Korisnik.objects.filter(korid=student1.korid).exists())
        self.assertFalse(Korisnik.objects.filter(korid=student2.korid).exists())

    def test_registracija_grupe_studenata_GET(self):
        response = self.client.get(reverse('upravljanje:registracija_grupe_studenata'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/registracija_grupe_studenata.html')

    def test_registracija_grupe_studenata_POST(self):
        content = 'korisnicko_ime,email,ime,prezime,lozinka,indeks\npera,nekimejl@gmail.com,Pera,Peric,12abcd34,2022/0182\nmarko,nekimejl@gmail.com,Marko,Markovic,12abcd34,2022/0183'

        dummy_file = SimpleUploadedFile(
            name='name.csv',
            content=bytes(content, encoding='utf-8'),
            content_type='text/plain'
        )
        response = self.client.post(reverse('upravljanje:registracija_grupe_studenata'), follow=True, data={
            'fajl': dummy_file
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{admin_path}/glavna.html')
        korisnik1 = Korisnik.objects.get(username='pera')
        korisnik2 = Korisnik.objects.get(username='marko')
        self.assertTrue(Student.objects.filter(korid=korisnik1))
        self.assertTrue(Student.objects.filter(korid=korisnik2))


class TestProfilTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        korisnik = Korisnik.objects.create_user(username='TestKorisnik',
                                                password='12abcd34',
                                                first_name='Pera',
                                                last_name='Peric',
                                                email='nekimejl@gmail.com')
        Student.objects.create(korid=korisnik,
                                jekapiten=0,
                                indeks='2022/0182')
        self.client.post(reverse('prijava'), data={
            'username': 'TestKorisnik',
            'password': '12abcd34',
        })

    def tearDown(self):
        self.client.get(reverse('odjava'))

    def test_prikaz_profila_GET(self):
        response = self.client.get(reverse('profil'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/profil.html')
        self.assertContains(response, 'TestKorisnik')
        self.assertContains(response, 'Pera')
        self.assertContains(response, 'Peric')
        self.assertContains(response, 'nekimejl@gmail.com')
        self.assertContains(response, '2022/0182')
        self.assertContains(response, 'student')

    def test_promena_lozinke_GET(self):
        response = self.client.get(reverse('promena_lozinke'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/promena_lozinke.html')

    def test_promena_lozinke_POST(self):
        response = self.client.post(reverse('promena_lozinke'), follow=True, data={
            'old_password': '12abcd34',
            'new_password1': 'ab1234cd',
            'new_password2': 'ab1234cd'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/profil.html')
        korisnik = Korisnik.objects.get(username='TestKorisnik')
        self.assertTrue(check_password('ab1234cd', korisnik.password))

    def test_promena_lozinke_fail_POST(self):
        response = self.client.post(reverse('promena_lozinke'), follow=True, data={
            'old_password': '12abcd34',
            'new_password1': 'ab1234cd',
            'new_password2': 'ab1234c'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{common_path}/promena_lozinke.html')
        korisnik = Korisnik.objects.get(username='TestKorisnik')
        self.assertTrue(check_password('12abcd34', korisnik.password))


class TestAdminBrowserTestCase(BaseSeleniumTest):

    def setUp(self):
        create_admin('Admin')
        korisnik = Korisnik.objects.get(username='Admin')
        korisnik.first_name = 'Admin'
        korisnik.last_name = 'Admincic'
        korisnik.save()

    def test_admin_browser(self):
        self.login('Admin', '/upravljanje')

        url = reverse('profil')
        link = self.driver.find_element(By.CSS_SELECTOR, f'a[href="{url}"]')
        link.click()
        time.sleep(1)

        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Promeni lozinku")]')
        submit.click()
        time.sleep(1)

        data = {
            'old_password': 'ab1234cd',
            'new_password1': '12abcd34',
            'new_password2': '12abcd34'
        }
        for name, key in data.items():
            self.driver.find_element(By.NAME, name).send_keys(key)
        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Promeni lozinku")]')
        submit.click()
        time.sleep(1)

        button = self.driver.find_element(By.XPATH, '//a[contains(., "Glavna")]')
        button.click()
        time.sleep(1)

        korisnik = Korisnik.objects.get(username='Admin')
        self.assertTrue(check_password('12abcd34', korisnik.password))

        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Registruj korisnika")]')
        submit.click()
        time.sleep(1)

        radio = self.driver.find_element(By.ID, 'asistent')
        radio.click()
        data = {
            'username': 'asistent',
            'email': 'nekimejl@gmail.com',
            'first_name': 'Asistent',
            'last_name': 'Asistentic',
            'password1': '12abcd34',
            'password2': '12abcd34'
        }
        for name, key in data.items():
            self.driver.find_element(By.NAME, name).send_keys(key)
        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Registruj")]')
        submit.click()
        time.sleep(1)

        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Registruj grupu studenata")]')
        submit.click()
        time.sleep(1)

        content = 'korisnicko_ime,email,ime,prezime,lozinka,indeks\n' \
                  'pera,nekimejl@gmail.com,Pera,Peric,12abcd34,2022/0182\n' \
                  'marko,nekimejl@gmail.com,Marko,Markovic,12abcd34,2022/0183\n' \
                  'mika, nekimejl@gmail.com,Mika,Mikic,12abcd34,2022/0184'
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_file.write(content)
        temp_file.flush()
        temp_file.close()
        file = self.driver.find_element(By.NAME, 'fajl')
        file.send_keys(temp_file.name)
        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Registruj")]')
        submit.click()
        time.sleep(1)

        self.assertIn('<td>asistent</td>', self.driver.page_source)
        self.assertIn('<td>pera</td>', self.driver.page_source)
        self.assertIn('<td>marko</td>', self.driver.page_source)
        self.assertIn('<td>mika</td>', self.driver.page_source)

        korisnik = Korisnik.objects.get(username='pera')

        row = self.driver.find_element(By.XPATH, f'//tr[@data-korid="{korisnik.korid}"]')
        button = row.find_element(By.TAG_NAME, 'button')
        button.click()
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        time.sleep(1)

        self.assertNotIn('<td>pera</td>', self.driver.page_source)

        button = self.driver.find_element(By.XPATH, '//button[contains(., "Izbriši sve studente")]')
        button.click()
        time.sleep(1)

        submit = self.driver.find_element(By.XPATH, '//button[contains(., "Da")]')
        submit.click()
        time.sleep(1)

        self.assertNotIn('<td>marko</td>', self.driver.page_source)
        self.assertNotIn('<td>mika</td>', self.driver.page_source)


class TestStudentAutoGroupTestCase(TestCase):
    def setUp(self):
        self.get_response = mock.MagicMock()
        self.middleware = AssignTeamsMiddleware(self.get_response)
        self.factory = RequestFactory()


    def test_student_group_phaze_zero_active(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() + timedelta(days=1), korid=asistent)

        create_student('TestStudent1', '2023/1111')
        create_student('TestStudent2', '2023/2222')
        create_student('TestStudent3', '2023/3333')

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 0)
        self.assertEqual(UTimu.objects.count(), 0)

    def test_student_single_teams(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1), korid=asistent)

        s1 = create_student('TestStudent1', '2023/1111')
        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        t2 = Tim.objects.create(nazivtima="TestTim2", imeprojekta="Projekat2", opisprojekta="")
        UTimu.objects.create(korid=s2, timid=t2)

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 1)
        self.assertEqual(Tim.objects.first().br_clanova, 2)
        self.assertEqual(UTimu.objects.count(), 2)

        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())

    def test_student_group_single_unassigned(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=asistent)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=s2, timid=t1)
        s3 = create_student('TestStudent3', '2023/3333')


        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 1)
        self.assertEqual(Tim.objects.first().br_clanova, 3)
        self.assertTrue(UTimu.objects.filter(korid=s3, timid=t1).exists())

        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())

    def test_student_group_2_unassigned(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=asistent)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=s2, timid=t1)
        s3 = create_student('TestStudent3', '2023/3333')
        s4 = create_student('TestStudent4', '2023/4444')

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 2)
        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())

    def test_student_group_3_unassigned(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=asistent)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=s2, timid=t1)
        s3 = create_student('TestStudent3', '2023/3333')
        s4 = create_student('TestStudent4', '2023/4444')
        s5 = create_student('TestStudent5', '2023/5555')

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 2)
        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())

    def test_student_group_4_unassigned(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=asistent)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=s2, timid=t1)
        s3 = create_student('TestStudent3', '2023/3333')
        s4 = create_student('TestStudent4', '2023/4444')
        s5 = create_student('TestStudent5', '2023/5555')
        s6 = create_student('TestStudent6', '2023/6666')

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 2)
        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())

    def test_student_group_5_unassigned(self):
        asistent = create_asistent("TestAsistent")
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=asistent)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=s2, timid=t1)
        s3 = create_student('TestStudent3', '2023/3333')
        s4 = create_student('TestStudent4', '2023/4444')
        s5 = create_student('TestStudent5', '2023/5555')
        s6 = create_student('TestStudent6', '2023/6666')
        s7 = create_student('TestStudent7', '2023/7777')

        self.middleware(self.factory.get("/"))

        self.assertEqual(Tim.objects.count(), 3)
        self.assertFalse(Student.objects.filter(utimu__isnull=True).exists())


class TestTeamListTestCase(BaseSeleniumTest):
    def setUp(self):
        self.asistent = create_asistent("TestAsistent")


        self.t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        self.s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=self.s1, timid=self.t1)
        self.s2 = create_student('TestStudent2', '2023/2222')
        UTimu.objects.create(korid=self.s2, timid=self.t1)
        self.s3 = create_student('TestStudent3', '2023/3333')
        self.s4 = create_student('TestStudent4', '2023/4444')

    def test_team_list_student_in_team(self):
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() + timedelta(days=1),
                               korid=self.asistent)

        self.login("TestStudent1", "/student")

        self.driver.get(f'{self.live_server_url}/lista_timova')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Već ste u timu')]"))
        )

    def test_team_list_student_unassigned(self):
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() + timedelta(days=1),
                               korid=self.asistent)

        self.login("TestStudent3", "/student")

        self.driver.get(f'{self.live_server_url}/lista_timova')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pridruži se')]"))
        )

    def test_team_list_student_unassigned_request_sent(self):
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() + timedelta(days=1),
                               korid=self.asistent)

        Zahteva.objects.create(korid=self.s3, timid=self.t1)
        self.login("TestStudent3", "/student")

        self.driver.get(f'{self.live_server_url}/lista_timova')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Već ste poslali zahtev ovom timu')]"))
        )

    def test_team_list_student_task_not_active(self):
        Zadatak.objects.create(brfaze=0, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=self.asistent)

        self.login("TestStudent3", "/student")

        self.driver.get(f'{self.live_server_url}/lista_timova')

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Formiranje timova nije dozvoljeno')]"))
        )


class TestDownloadProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        asistent = create_asistent("TestAsistent")
        self.zadatak = Zadatak.objects.create(brfaze=1, naslov="Zadatak1", tekst="", rok=timezone.now() + timedelta(days=1),
                               korid=asistent)

        self.t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="", timid=12345678,)
        self.s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=self.s1, timid=self.t1)


    def test_student_download_project_not_found(self):
        self.client.post(reverse('prijava'), data={
            'username': 'TestStudent1',
            'password': 'ab1234cd'
        })
        response = self.client.get(reverse('preuzimanje_projekta', kwargs={'timid': self.t1.timid}))
        self.assertEqual(response.status_code, 404)

    def test_student_download_project_success(self):
        self.client.post(reverse('prijava'), data={
            'username': 'TestStudent1',
            'password': 'ab1234cd'
        })
        folder = f'{projekti_path}/latest/tim_{self.t1.timid}'
        Path(folder).mkdir(parents=True, exist_ok=True)
        with open(f"{folder}/test.txt", "w") as f:
            f.write("test")
        Projekat.objects.create(folder=folder, updatum=timezone.now(), timid=self.t1)

        response = self.client.get(reverse('preuzimanje_projekta', kwargs={'timid': self.t1.timid}))
        self.assertEqual(
            response.get('Content-Disposition'),
            f"attachment; filename=\"{self.t1.nazivtima}_latest.zip\""
        )
        shutil.rmtree(folder)

    def test_asistent_download_project_not_found(self):
        self.client.post(reverse('prijava'), data={
            'username': 'TestAsistent',
            'password': 'ab1234cd'
        })
        response = self.client.get(reverse('asistent:preuzimanje_projekta', kwargs={
            'timid': self.t1.timid,
            'zadid': self.zadatak.zadid
        }))
        self.assertEqual(response.status_code, 404)

    def test_asistent_download_project_success(self):
        self.client.post(reverse('prijava'), data={
            'username': 'TestAsistent',
            'password': 'ab1234cd'
        })
        folder = f'{projekti_path}/zadatak_{self.zadatak.zadid}/tim_{self.t1.timid}'
        Path(folder).mkdir(parents=True, exist_ok=True)
        with open(f"{folder}/test.txt", "w") as f:
            f.write("test")

        response = self.client.get(reverse('asistent:preuzimanje_projekta', kwargs={
            'timid': self.t1.timid,
            'zadid': self.zadatak.zadid
        }))

        self.assertEqual(
            response.get('Content-Disposition'),
            f"attachment; filename=\"zadatak_{self.zadatak.zadid}_{self.t1.nazivtima}.zip\""
        )
        shutil.rmtree(folder)

    def tearDown(self):
        self.client.get(reverse('odjava'))

class TestSendAnnouncementsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.korisnik = Korisnik.objects.create(username='TestKorisnik')
        self.korisnik.set_password('12abcd34')
        self.korisnik.save()
        Asistent.objects.create(korid=self.korisnik)
        self.client.login(username='TestKorisnik', password='12abcd34')

    def tearDown(self):
        self.client.post(reverse('odjava'))

    def test_send_announcements(self):
        response = self.client.post(reverse('asistent:kreiranje_obavestenja'), follow=True, data={
            'naslov': 'test',
            'tekst': 'Ovo je test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/glavna.html')
        self.assertEqual(Obavestenje.objects.count(), 1)
        self.assertEqual(Primio.objects.count(), 1)


class TestCheckAnnouncementsTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.appUrl = self.live_server_url + '/prijava'

    def tearDown(self):
        self.browser.close()

    def test_check_announcements(self):
        user = Korisnik.objects.create(username='pera')
        user.set_password('ab1234cd')
        Student.objects.create(korid = user)
        user.is_active = True
        user.save()
        self.browser.get(self.appUrl)
        text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Prijava', text)
        username = self.browser.find_element(By.NAME, 'username')
        username.send_keys("pera")
        password = self.browser.find_element(By.NAME, 'password')
        password.send_keys("ab1234cd")
        button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        button.click()
        time.sleep(5)
        button = self.browser.find_element(By.CSS_SELECTOR, "a[href='/prikaz_obavestenja']")
        button.click()
        time.sleep(5)
        text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Obavestenja', text)
        button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        button.click()
        time.sleep(5)


class TestUploadProject(TestCase):
    def setUp(self):
        self.client = Client()
        self.korisnik = Korisnik.objects.create(username='TestKorisnik')
        self.korisnik.set_password('12abcd34')
        self.korisnik.save()
        s = Student.objects.create(korid=self.korisnik)
        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        UTimu.objects.create(korid=s, timid=t1)
        self.client.login(username='TestKorisnik', password='12abcd34')

    def tearDown(self):
        self.client.post(reverse('odjava'))

    def test_send_announcements(self):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('folder/test.txt', 'Ovo je test')
        zip_buffer.seek(0)
        uploaded_zip = SimpleUploadedFile(
            name='test_proj.zip',
            content=zip_buffer.getvalue(),
            content_type='application/zip'
        )
        url = reverse('student:cuvanje_projekta')
        response = self.client.post(
            url,
            data={'file': uploaded_zip},
            format='multipart'
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Projekat.objects.count(), 1)


class TestGrade(TestCase):
    def setUp(self):
        self.client = Client()
        self.korisnik = Korisnik.objects.create(username='TestKorisnik')
        self.korisnik.set_password('12abcd34')
        self.korisnik.save()

        self.client.login(username='TestKorisnik', password='12abcd34')

    def tearDown(self):
        self.client.post(reverse('odjava'))

    def test_grade(self):
        a = Asistent.objects.create(korid=self.korisnik)
        z = Zadatak.objects.create(brfaze=1, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                                   korid=a)

        t1 = Tim.objects.create(nazivtima="TestTim1", imeprojekta="Projekat1", opisprojekta="")
        s1 = create_student('TestStudent1', '2023/1111')
        UTimu.objects.create(korid=s1, timid=t1)
        Projekat.objects.create(timid=t1, updatum=timezone.now() - timedelta(days=2))
        response = self.client.post(reverse(
            'asistent:ocenjivanje_resenja',
            kwargs={
                'tim_id': t1.timid,
                'zad_id': z.zadid,
            }
        ), follow=True, data={
            'bodovi': '50',
            'komentar': 'Ovo je test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/tabela_resenja.html')
        self.assertEqual(Ocena.objects.count(), 1)
        self.assertEqual(Obavestenje.objects.count(), 1)

class TestCheckSolution(BaseSeleniumTest):

    def setUp(self):
        self.client = Client()
        self.asistent = create_asistent("TestAsistent")
        self.student = create_student('TestStudent1', '2023/1111')

        self.zadatak = Zadatak.objects.create(brfaze=1, naslov="", tekst="", rok=timezone.now() - timedelta(days=1),
                               korid=self.asistent)

        self.tim = Tim.objects.create(nazivtima='PSI_Tim', imeprojekta='PSI_Projekat')
        UTimu.objects.create(korid=self.student, timid=self.tim)
        Projekat.objects.create(timid=self.tim, updatum=timezone.now() - timedelta(days=2))

    def test_check_solution(self):
        self.login("TestAsistent", "/asistent")
        url = reverse('asistent:prikaz_resenja_zadatka', kwargs={'tim_id': self.tim.timid,'zad_id': self.zadatak.zadid})
        self.driver.get(f'{self.live_server_url}{url}')
        time.sleep(1)
        detail_url = reverse(
            'asistent:prikaz_resenja_zadatka',
            kwargs={'tim_id': self.tim.timid,
                    'zad_id': self.zadatak.zadid}
        )
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(detail_url)
        )

class TestKreiranjeObavestenjaTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.asistent = create_asistent('TestAsistent')
        self.student = create_student('TestStudent', '2021/0504')

        self.client.post(reverse('prijava'), data={
            'username': 'TestAsistent',
            'password': 'ab1234cd'
        })

    def tearDown(self):
        self.client.get(reverse('odjava'))

    def test_kreiranje_obavestenja_GET(self):
        response = self.client.get(reverse('asistent:kreiranje_obavestenja'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/kreiranje_obavestenja.html')

    def test_kreiranje_obavestenja_POST(self):
        response = self.client.post(reverse('asistent:kreiranje_obavestenja'), follow=True, data={
            'naslov': 'Naslov',
            'tekst': 'Tekst'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/glavna.html')

        self.assertTrue(Obavestenje.objects.filter(naslov='Naslov').exists())
        novo_obavestenje = Obavestenje.objects.get(naslov='Naslov')

        # Provera da li su i asistent i student u tabeli Primio
        self.assertEqual(Primio.objects.filter(obid=novo_obavestenje).count(), 2)
        prijem_student = Primio.objects.get(korid=self.student.korid, obid=novo_obavestenje)
        self.assertFalse(prijem_student.procitano)

    def test_kreiranje_obavestenja_gost_GET(self):
        self.client.logout()
        response = self.client.get(reverse('asistent:kreiranje_obavestenja'))
        self.assertNotEqual(response.status_code, 200)

    def test_kreiranje_obavestenja_gost_POST(self):
        self.client.logout()
        response = self.client.post(reverse('asistent:kreiranje_obavestenja'), data={
            'naslov': 'Lose',
            'tekst': 'Lose'
        })
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Obavestenje.objects.filter(naslov='Lose').exists())


class TestKreiranjeZadatkaTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.asistent = create_asistent('TestAsistent')
        self.student = create_student('TestStudent', '2021/0504')

        self.client.post(reverse('prijava'), data={
            'username': 'TestAsistent',
            'password': 'ab1234cd'
        })

    def tearDown(self):
        self.client.get(reverse('odjava'))

    def test_kreiranje_zadatka_GET(self):
        response = self.client.get(reverse('asistent:kreiranje_zadatka'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/kreiranje_zadatka.html')

    def test_kreiranje_zadatka_nulta_faza_POST(self):
        response = self.client.post(reverse('asistent:kreiranje_zadatka'), follow=True, data={
            'naslov': 'Projekat Faza 0',
            'tekst': 'Tekst zadatka 0',
            'rok': '2026-12-31 23:59:00',
            'brfaze': 0
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/glavna.html')

        self.assertTrue(Zadatak.objects.filter(naslov='Projekat Faza 0').exists())

        self.assertTrue(Obavestenje.objects.filter(naslov='Projekat Faza 0').exists())
        novo_obavestenje = Obavestenje.objects.get(naslov='Projekat Faza 0')

        #Provera da samo student prim obavestenje a asistent ne
        self.assertTrue(Primio.objects.filter(korid=self.student.korid, obid=novo_obavestenje).exists())
        self.assertFalse(Primio.objects.filter(korid=self.asistent.korid, obid=novo_obavestenje).exists())

    @mock.patch('app.views.asistent.Path.mkdir')
    def test_kreiranja_zadatka_nenulta_faza_POST(self, mock_mkdir):
        Tim.objects.create(nazivtima='PSI_Tim', imeprojekta='PSI_Projekat')

        response = self.client.post(reverse('asistent:kreiranje_zadatka'), follow=True, data={
            'naslov': 'Projekat Faza 1',
            'tekst': 'Tekst zadatka 1',
            'rok': '2026-12-31 23:59:00',
            'brfaze': 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'{asistent_path}/glavna.html')

        self.assertTrue(Zadatak.objects.filter(naslov='Projekat Faza 1').exists())

        self.assertTrue(Obavestenje.objects.filter(naslov='Projekat Faza 1').exists())
        novo_obavestenje = Obavestenje.objects.get(naslov='Projekat Faza 1')

        # Provera da samo student prim obavestenje a asistent ne
        self.assertTrue(Primio.objects.filter(korid=self.student.korid, obid=novo_obavestenje).exists())
        self.assertFalse(Primio.objects.filter(korid=self.asistent.korid, obid=novo_obavestenje).exists())

        #Provera da li pravi potrebne foldere
        self.assertTrue(mock_mkdir.called)
        self.assertEqual(mock_mkdir.call_count, 2)

    def test_kreiranje_zadatka_gost_GET(self):
        self.client.logout()
        response = self.client.get(reverse('asistent:kreiranje_zadatka'))
        self.assertNotEqual(response.status_code, 200)

    def test_kreiranje_zadatka_gost_POST(self):
        self.client.logout()
        response = self.client.post(reverse('asistent:kreiranje_zadatka'), data={
            'naslov': 'Lose',
            'tekst': 'Lose',
            'rok': '2026-12-31 23:59:00',
            'brfaze': 0
        })

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Zadatak.objects.filter(naslov='Lose').exists())


class TestAzuriranjeTimaTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.moj_tim = Tim.objects.create(
            nazivtima='Tim1',
            imeprojekta='Projekat1',
            opisprojekta='Opis1'
        )
        self.student = create_student('TestStudent', '2021/0504')
        self.student.jekapiten = 1
        self.student.save()

        UTimu.objects.create(korid=self.student, timid=self.moj_tim)

        self.drugi_tim = Tim.objects.create(
            nazivtima='Tim2',
            imeprojekta='Projekat2',
            opisprojekta='Opis2'
        )

        self.client.post(reverse('prijava'), data={
            'username': 'TestStudent',
            'password': 'ab1234cd'
        })

    def tearDown(self):
        self.client.logout()

    def test_azuriranje_tima_GET(self):
        response = self.client.get(reverse('student:azuriranje_tima'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/student/azuriranje_tima.html')

        form = response.context['form']
        self.assertEqual(form.initial['nazivtima'], self.moj_tim.nazivtima)
        self.assertEqual(form.initial['imeprojekta'], self.moj_tim.imeprojekta)
        self.assertEqual(form.initial['opisprojekta'], self.moj_tim.opisprojekta)

    def test_azuriranje_tima_uspesan_POST(self):

        response = self.client.post(reverse('student:azuriranje_tima'), data={
            'nazivtima': 'NoviNaziv',
            'imeprojekta': 'NoviProjekat',
            'opisprojekta': 'NoviOpis'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/tim.html')

        self.moj_tim.refresh_from_db()
        self.assertEqual(self.moj_tim.nazivtima, 'NoviNaziv')
        self.assertEqual(self.moj_tim.imeprojekta, 'NoviProjekat')
        self.assertEqual(self.moj_tim.opisprojekta, 'NoviOpis')

    def test_azuriranje_tima_konflikt_naziv_tima_POST(self):
        response = self.client.post(reverse('student:azuriranje_tima'), data={
            'nazivtima': 'Tim2',
            'imeprojekta': 'Blabla',
            'opisprojekta': 'Blabla'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/student/azuriranje_tima.html')
        self.assertEqual(response.context['poruka'], 'Tim sa tim imenom već postoji.')

        self.moj_tim.refresh_from_db()
        self.assertEqual(self.moj_tim.nazivtima, 'Tim1')

    def test_azuriranje_tima_konflikt_ime_projekta_POST(self):
        response = self.client.post(reverse('student:azuriranje_tima'), data={
            'nazivtima': 'Slobodan',
            'imeprojekta': 'Projekat2',
            'opisprojekta': 'Blabla'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/student/azuriranje_tima.html')
        self.assertEqual(response.context['poruka'], 'Tim sa tim imenom projekta već postoji.')

        self.moj_tim.refresh_from_db()
        self.assertEqual(self.moj_tim.imeprojekta, 'Projekat1')

    def test_azuriranje_tima_gost_GET(self):
        self.client.logout()

        response = self.client.get(reverse('student:azuriranje_tima'))

        self.assertNotEqual(response.status_code, 200)


class TestSlanjeZahtevaTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.tim = Tim.objects.create(
            nazivtima='TestTim',
            imeprojekta='TestProjekat'
        )

        kapiten_korisnik = Korisnik.objects.create(username='Kapiten', first_name='Ime', last_name='Prezime')
        kapiten_korisnik.set_password('ab1234cd')
        kapiten_korisnik.save()
        self.kapiten = Student.objects.create(korid=kapiten_korisnik, indeks='2021/0001', jekapiten=1)
        UTimu.objects.create(korid=self.kapiten, timid=self.tim)


        self.student = create_student('Student', '2021/0002')
        self.client.post(reverse('prijava'), data={
            'username': 'Student',
            'password': 'ab1234cd'
        })

    def tearDown(self):
        self.client.logout()

    def test_uspesno_slanje_zahteva(self):
        response = self.client.post(reverse('student:zahtev'), data={
            'timid': self.tim.timid
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/student/zahtev_poslat.html')
        self.assertIn('Zahtev za pridruživanje timu je poslat', response.context['poruka'])

        self.assertTrue(Zahteva.objects.filter(korid=self.student, timid=self.tim).exists())

        obavestenje_postoji = Obavestenje.objects.filter(naslov='Zahtev za učlanjenje').exists()
        self.assertTrue(obavestenje_postoji)

class TestObradaZahtevaTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.tim = Tim.objects.create(
            nazivtima='Tim',
            imeprojekta='Projekat'
        )

        self.kapiten = create_student('Kapiten', '2021/0010')
        self.kapiten.jekapiten = 1
        self.kapiten.save()

        UTimu.objects.create(korid=self.kapiten, timid=self.tim)

        self.student = create_student('Student', '2021/0011')

        self.zahtev = Zahteva.objects.create(korid=self.student, timid=self.tim)

        self.client.post(reverse('prijava'), data={
            'username': 'Kapiten',
            'password': 'ab1234cd'
        })

    def tearDown(self):
        self.client.logout()

    def test_prihvatanje_zahteva_uspesno(self):
        Zahteva.objects.create(korid=self.student, timid=self.tim)

        url = reverse('student:obrada_zahteva', kwargs={'korid': self.student.korid.korid})
        response = self.client.post(url, data={'prihvacen': 1})

        ocekivani_url = reverse('prikaz_tima', kwargs={'timid': self.tim.timid})
        self.assertRedirects(response, ocekivani_url)

        self.assertTrue(UTimu.objects.filter(korid=self.student, timid=self.tim).exists())

        self.assertFalse(Zahteva.objects.filter(korid=self.student, timid=self.tim).exists())

        obavestenje = Obavestenje.objects.filter(naslov='Zahtev je prihvacen').latest('obid')
        self.assertTrue(Primio.objects.filter(korid=self.student.korid, obid=obavestenje).exists())


class TestPrikazZadatakaTestCase(BaseSeleniumTest):

    def setUp(self):
        self.asistent = create_asistent("Asistent")

        self.aktivan_zadatak = Zadatak.objects.create(
            naslov="AktivniZadatak",
            tekst="Ovaj zadatak je aktivan!!!",
            brfaze=1,
            rok=timezone.now() + timedelta(days=5),
            korid=self.asistent
        )

        self.istekao_zadatak = Zadatak.objects.create(
            naslov="IstekliZadatak",
            tekst="Ovom zadatku je prosao!",
            brfaze=2,
            rok=timezone.now() - timedelta(days=2),
            korid=self.asistent
        )

        self.student = create_student("Student", "2021/0504")

    def test_student_vidi_samo_aktivne_zadatke(self):
        self.login("Student", "/student")

        self.driver.get(f"{self.live_server_url}/student")

        # Provera da student vidi aktivan zadaak
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.aktivan_zadatak.naslov}')]"))
        )

        # Provera da student ne vidi zadatak kome je istekao rok
        istekli_elementi = self.driver.find_elements(By.XPATH,
                                                     f"//*[contains(text(), '{self.istekao_zadatak.naslov}')]")
        self.assertEqual(len(istekli_elementi), 0, "Student vidi zadatak kome je istekao rok!")

    def test_asistent_vidi_sve_zadatke(self):
        self.login("Asistent", "/asistent")
        self.driver.get(f"{self.live_server_url}/asistent")


        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.aktivan_zadatak.naslov}')]"))
        )

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{self.istekao_zadatak.naslov}')]"))
        )
