from django.contrib.sitemaps import Sitemap
from django.apps import apps
from django.urls import reverse

Housing = apps.get_model('app_housing', 'HousingObject')


class RealEstateStaticSitemap(Sitemap):
    changefreq = 'dayly'
    priority = 0.9

    def items(self):
        return ['about', 'contacts']

    def location(self, item):
        return reverse(item)


class RealEstateDynamicSitemap(Sitemap):
    changefreq = 'dayly'
    priority = 0.9

    def items(self):
        return Housing.objects.all()
