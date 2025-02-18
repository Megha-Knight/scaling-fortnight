from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class LabConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lab"

from django.apps import AppConfig

class LabConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lab"

    def ready(self):
        import lab.signals  # Import signals when the app is ready

