import sys
import threading
import time

from django.apps import AppConfig
from pathlib import Path


def init_folders():
    """
    Inicijalizacija folder strukture na osnovu podatak u bazi
    """
    time.sleep(1)
    from app.models import Zadatak, Tim
    zadaci = Zadatak.objects.all()
    timovi = Tim.objects.all()
    Path('projekti/latest').mkdir(parents=True, exist_ok=True)
    for tim in timovi:
        Path(f'projekti/latest/tim_{tim.timid}').mkdir(parents=True, exist_ok=True)
    for zadatak in zadaci:
        if zadatak.je_formiranje_timova:
            continue
        Path(f'projekti/zadatak_{zadatak.zadid}').mkdir(exist_ok=True)
        for tim in timovi:
            Path(f'projekti/zadatak_{zadatak.zadid}/tim_{tim.timid}').mkdir(exist_ok=True)


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        """
        Redefinicija metode ready() da bi folderi za projekte garantovano postojali za svaki tim kad se aplikacija pokrene
        """
        if 'test' in sys.argv:
            return

        threading.Thread(target=init_folders, daemon=True).start()
