from django.apps import AppConfig


class ZyloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zylo'

    def ready(self):
        import zylo.signals

