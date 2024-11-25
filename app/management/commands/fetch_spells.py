from django.core.management.base import BaseCommand
from app.views import fetch_spells_from_api

class Command(BaseCommand):
    help = 'Fetch spells from the API and populate the database'

    def handle(self, *args, **kwargs):
        fetch_spells_from_api()
        self.stdout.write(self.style.SUCCESS('Successfully fetched spells from the API'))
