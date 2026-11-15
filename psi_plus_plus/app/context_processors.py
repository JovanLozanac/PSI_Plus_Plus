from app.models import Korisnik
from app.views import common

#Autor Artjom Uljanov 2023/0421
#Autor David Radivojevic 2021/0504

def user_context(request):
    if not request.user.is_authenticated:
        return {}

    return {
        'admin': getattr(request.user, 'admin', None),
        'asistent': getattr(request.user, 'asistent', None),
        'student': getattr(request.user, 'student', None),
        'broj_neprocitanih': common.dohvati_broj_neprocitanih(request.user)
    }

