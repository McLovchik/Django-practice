from django.contrib import admin
from .models import HousingObject, HousingType, RoomsNumberInHousingObject


class HousingObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class HousingTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']


class RoomsNumberInHousingObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity']


admin.site.register(HousingObject, HousingObjectAdmin)
admin.site.register(HousingType, HousingTypeAdmin)
admin.site.register(RoomsNumberInHousingObject, RoomsNumberInHousingObjectAdmin)
