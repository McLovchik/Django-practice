from django.db import models
from django.utils.translation import gettext_lazy as _


class File(models.Model):
    file = models.FileField(upload_to='files/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _('files')
        verbose_name = _('file')
