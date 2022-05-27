from django.apps import AppConfig


class RestodappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RestoDApp'
    def ready(self):
        import RestoDApp.signals
