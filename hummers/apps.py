from django.apps import AppConfig


class HummersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hummers'

    def ready(self):
        from . import signals
