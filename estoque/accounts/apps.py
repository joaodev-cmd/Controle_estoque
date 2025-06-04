from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib.auth.models import Group
        group_names = ['fisioterapeuta', 'administrador']
        for name in group_names:
            Group.objects.get_or_create(name=name)
