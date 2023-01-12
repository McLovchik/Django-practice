from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Record(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'),
                               blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('date create'))
    text = models.TextField(verbose_name=_('text'))

    def __str__(self):
        return f'{self.text[:25]}...'

    class Meta:
        verbose_name_plural = _('records')
        verbose_name = _('record')


class RecordImage(models.Model):
    image = models.ImageField(upload_to='records/', blank=True, null=True)
    record = models.ForeignKey('Record', on_delete=models.CASCADE, verbose_name='Запись')
