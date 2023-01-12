from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    code = models.CharField(max_length=32, verbose_name=_('article'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))

    class Meta:
        verbose_name_plural = _('goods')


class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('loyalty programs')
        verbose_name = _('loyalty program')


class Promotion(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('promotions')
        verbose_name = _('promotion')


class Offer(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('offers')
        verbose_name = _('offer')
