from django.contrib.sitemaps import Sitemap
from .models import NewsItem


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    #  атрибуты changefreq и priority указывают на чистоту изменения страниц с постами их релевантность на сайте

    def items(self):
        """Возвращает queryset объектов модели, которые должны попасть в карту сайта"""
        return NewsItem.objects.filter(is_published=True).all()

    def lastmod(self, obj: NewsItem):
        """Получает каждый объект, который вернул метод items и свою очередь возвращает дату, когда тот последний раз изменялся"""
        return obj.published_at
