from django.apps import AppConfig


class InstitucionalConfig(AppConfig):
    name = 'apps.institucional'

    def ready(self):
        import apps.institucional.signals
