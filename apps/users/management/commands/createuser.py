from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from forgery_py import internet
from forgery_py import name

from utils.helpers import fetch_random_image


class Command(BaseCommand):
    help = 'Creates random users.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--count',
            nargs='?',
            type=int,
            default=5,
            help='Number of users to create. Default is 5.',
        )

    def handle(self, *args, **options):

        try:
            self.count = options['count']
            User = get_user_model()

            for i in range(self.count):
                user = User.objects.create(
                    email=internet.email_address(),
                    first_name=name.first_name(),
                    last_name=name.last_name(),
                    password="solsolsol",
                )

                user.picture = fetch_random_image(f"vignette_{user.full_name}")
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created user {user}'))

        except (IntegrityError, CommandError):
            self.stdout.write(
                self.style.WARNING(
                    'User "%s" already exists.' % 'admin'))
