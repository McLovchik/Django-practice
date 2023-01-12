from django.db import models
from django.urls import reverse


class NewsItem(models.Model):
    title = models.CharField(max_length=1000, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст записи')
    is_published = models.BooleanField(default=False)
    type = models.ForeignKey('NewsType', on_delete=models.CASCADE, null=True)
    description = models.TextField(verbose_name='описание', default='')
    published_at = models.DateTimeField(verbose_name='дата публикации', null=True)

    def get_absolute_url(self):
        return reverse('news-item', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class NewsType(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'название')
    code = models.CharField(max_length=32, verbose_name=u'код')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тип новости'
        verbose_name_plural = 'типы новостей'
