from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'apps._example'

    def ready(self):
        import apps.articles.signals
