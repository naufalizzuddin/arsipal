from django.apps import AppConfig


class ArsipDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arsip_database'

    def ready(self):
        import arsip_database.signals
        return super().ready()