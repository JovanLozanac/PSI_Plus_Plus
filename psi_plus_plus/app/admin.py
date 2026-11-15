from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Korisnik, Admin, Asistent, Student

admin.site.register(Korisnik, UserAdmin)

admin.site.register(Admin)

admin.site.register(Asistent)

admin.site.register(Student)