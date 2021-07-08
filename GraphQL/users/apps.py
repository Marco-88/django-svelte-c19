from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = ('profiles')

    def ready(self):
        import users.signals

