from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        try:
            from django.contrib.auth.models import Group
            group_names = ['fisioterapeuta', 'administrador']
            for name in group_names:
                Group.objects.get_or_create(name=name)
        except Exception:
            # Ignora erro caso o banco ainda não esteja pronto (ex: antes das migrations)
            pass
