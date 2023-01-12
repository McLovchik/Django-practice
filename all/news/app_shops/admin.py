from django.contrib import admin

from .models import Shop, Product, ProductInShop, Cart, Purchase


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Shop, ShopAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


admin.site.register(Product, ProductAdmin)


class ProductInShopAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'quantity',)


admin.site.register(ProductInShop, ProductInShopAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'product', 'quantity',)


admin.site.register(Cart, CartAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'cost')


admin.site.register(Purchase, PurchaseAdmin)
