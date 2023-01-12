from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))

    class Meta:
        verbose_name_plural = _('shops')
        verbose_name = _('shop')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='product name')
    price = models.PositiveIntegerField(verbose_name='price')
    shops = models.ManyToManyField(Shop, through='ProductInShop', related_name='shops')

    class Meta:
        verbose_name_plural = 'products'
        verbose_name = 'product'

    def __str__(self):
        return self.name


class ProductInShop(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='quantity')

    class Meta:
        verbose_name_plural = 'products in shop'
        verbose_name = 'product in shop'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity')

    @property
    def total_cost(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name_plural = 'carts'
        verbose_name = 'cart'

    def __str__(self):
        return self.product.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity')
    cost = models.PositiveIntegerField(verbose_name='cost')

    class Meta:
        verbose_name_plural = 'purchases'
        verbose_name = 'purchase'
