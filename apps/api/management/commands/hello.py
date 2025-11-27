from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hello"

    def handle(self, *args, **options):
        self.stdout.write(f"Hello {settings.FOO}")
