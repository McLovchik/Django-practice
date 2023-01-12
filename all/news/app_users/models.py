import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from app_goods.models import LoyaltyProgram, Offer
import logging

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=36, blank=True, verbose_name=_('city'))
    phone = models.CharField(max_length=11, blank=True, verbose_name=_('phone'))
    # verification_flag = models.BooleanField(default=False, verbose_name='Флаг верификации')
    count_news = models.IntegerField(default=0, verbose_name=_('count public news'))

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (
            ('can_verify_user', 'Может верифицировать пользователя'),
            ('can_activate_news', 'Может активировать новость')
        )
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')


class PersonalCabinet(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, verbose_name=_('balance'))
    # promotions = models.ManyToManyField(Promotion, symmetrical=False)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,
                              verbose_name=_('offer'), blank=True, null=True)
    loyalty_program_item = models.ForeignKey(LoyaltyProgram, on_delete=models.SET_NULL,
                                             verbose_name=_('loyalty program item'), blank=True, null=True)
    status_points = models.IntegerField(default=0, verbose_name='status')

    @property
    def status(self):
        if self.status_points > 1000:
            logger.info(f'Пользователь {self.profile.user.username} перешел на статус - Platinum')
            return 'Platinum'
        elif self.status_points > 500:
            logger.info(f'Пользователь {self.profile.user.username} перешел на статус - Gold')
            return 'Gold'
        elif self.status_points > 100:
            logger.info(f'Пользователь {self.profile.user.username} перешел на статус - Silver')
            return 'Silver'
        return 'No status'

    class Meta:
        verbose_name_plural = _('personal cabinets')
        verbose_name = _('personal cabinet')
