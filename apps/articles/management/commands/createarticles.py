import random
from random import randint

import forgery_py
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from requests import get

from apps.articles.models import Article
from apps.articles.models import Category
from apps.users.models import User
from utils.helpers import fetch_random_image
from utils.helpers import generate_random_img_url


LOREM = forgery_py.lorem_ipsum


class Command(BaseCommand):
    help = 'Creates articles and categories with random content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--articles',
            nargs='?',
            type=int,
            default=5,
            help='Max number of articles per category. Default is 5.',
        )

        parser.add_argument(
            '-c',
            '--categories',
            nargs='?',
            type=int,
            default=5,
            help='Amount of categories. Default is 5.',
        )

        parser.add_argument(
            '--clear',
            nargs='?',
            type=bool,
            default=True,
            help='Clear all categories/articles.',
        )

        parser.add_argument(
            '--count',
            nargs='?',
            type=bool,
            default=True,
            help='Number of existing categories/articles.',
        )

        parser.add_argument(
            '--isEmpty',
            nargs='?',
            type=bool,
            default=True,
            help='Used internaly.',
        )

    def handle(self, *args, **options):
        try:
            self.c_count = options['categories']
            self.a_count = options['articles']
            self.is_empty = not options['isEmpty']
            self.clear = not options['clear']
            self.count = not options['count']
            # self.debug()

            if self.count:
                self.action_count()
            elif self.clear:
                self.action_clear()
            elif self.is_empty:
                self.action_is_empty()
            else:
                self.action_create()

        except (IntegrityError, CommandError) as e:
            self.error_message(e)

    def action_count(self):
        c_count = Category.objects.count()
        a_count = Article.objects.count()
        highlighted = len(Article.objects.filter(highlighted=True))
        self.stdout.write(
            self.style.WARNING(
                (f"Categories count: {c_count}\n"
                 f"Articles count: {a_count}\n"
                 f"Highlighted articles: {highlighted}")))

    def action_clear(self):
        for category in Category.objects.all():
            category.delete()

    def action_is_empty(self):
        return self.stdout.write("0" if Article.objects.count() else "1")

    def action_create(self):
        for categories in range(self.c_count):
            name = forgery_py.internet.domain_name().split(".")[0]
            category = Category.objects.create(
                name=name.capitalize(),
                description=forgery_py.lorem_ipsum.sentences(5),
                published=True
            )
            a_count = randint(3, self.a_count)
            self.success_message(
                f'\033[1mCategory\033[0m "{category.name}" '
                f'\033[92mcreated\033[0m ({a_count} articles).')

            for i in range(a_count):
                article_content = self.create_article()
                image_name = "{}_{}".format(name, str(i).zfill(2))
                article = Article.objects.create(
                    highlighted=not randint(0, 2),
                    published=True,
                    image=fetch_random_image(image_name),
                    category=category,
                    title=article_content['title'],
                    description=article_content['description'],
                    body=article_content['body'],
                    author=random.choice(User.objects.all())
                )
                self.success_message(
                    f'\t\033[1mArticle\033[0m "{article.title}"'
                    f' \033[92mcreated\033[0m.')

    def create_article(self):
        api_args = "?no-code=on"
        api = f"{settings.LOREM_API}{api_args}"

        splitted_text = get(api).text.split("\n")
        article = {
            'title': " ".join(splitted_text[0]
                              .replace("#", "")
                              .lstrip()
                              .split(" ")[:randint(2, 3)]),
            'description': forgery_py.lorem_ipsum.sentence(),
            'body': []
        }
        for line in splitted_text[4:]:
            if line == "" and not randint(0, 5):
                width = randint(320, 720)
                height = int(width // 1.5)
                image = generate_random_img_url(width, height)
                article['body'].append(f"\n![]({image})\n")
            else:
                article['body'].append(line)

        article['body'] = "\n".join(article['body'])
        return article

    def success_message(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def error_message(self, message):
        self.stdout.write(self.style.ERROR(message))

    def debug(self):
        args = ["c_count", "a_count", "clear", "count", "is_empty"]
        print("\n".join([f"{i}: {getattr(self, i)}" for i in args]))
