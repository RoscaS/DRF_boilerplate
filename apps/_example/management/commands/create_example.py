import forgery_py
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.utils import IntegrityError

from apps._example.models import Example


LOREM = forgery_py.lorem_ipsum


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--example',
            nargs='?',
            type=int,
            default=5,
            help='',
        )


    def handle(self, *args, **options):
        try:
            self.example = options['example']

            example = Example.objects.create(name="Example")
            example.save()

            self.stdout.write(self.style.SUCCESS("Example created"))


        except (IntegrityError, CommandError) as e:
            self.stdout.write(self.style.ERROR(e))
