from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'apps.articles'

    def ready(self):
        import apps.articles.signals
