from django.db import models
from django.urls import reverse


class HousingObject(models.Model):
    title = models.CharField(max_length=128, verbose_name='заголовок')
    description = models.TextField(default='', blank=True, verbose_name='описание')
    type = models.ForeignKey('HousingType', on_delete=models.CASCADE, null=True, blank=True)
    rooms_number = models.ForeignKey('RoomsNumberInHousingObject', on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('real_estate_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'жильё'
        verbose_name_plural = 'жильё'


class HousingType(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    code = models.CharField(max_length=32, verbose_name='код')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тип жилья'
        verbose_name_plural = 'типы жилья'


class RoomsNumberInHousingObject(models.Model):
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество комнат')
