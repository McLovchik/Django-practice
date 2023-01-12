from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppRecordsConfig(AppConfig):
    name = 'app_records'
    verbose_name = _('records')
