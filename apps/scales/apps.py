from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScalesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scales"
    verbose_name = "Шкалы"
