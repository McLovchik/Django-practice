from django.contrib import admin
from .models import Item, LoyaltyProgram, Promotion, Offer


class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'price')


admin.site.register(Item, ItemAdmin)


class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(LoyaltyProgram, LoyaltyProgramAdmin)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Promotion, PromotionAdmin)


class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Offer, OfferAdmin)
