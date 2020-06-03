from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'apps._examples'

    def ready(self):
        import apps.articles.signals
