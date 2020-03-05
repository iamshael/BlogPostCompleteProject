from django.apps import AppConfig


class UserappConfig(AppConfig):
    name = 'userapp'

    def ready(self):
        import userapp.signals
