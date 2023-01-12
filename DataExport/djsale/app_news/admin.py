from django.contrib import admin
from .models import NewsItem, NewsType


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(NewsItem, NewsItemAdmin)


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']


admin.site.register(NewsType, NewsTypeAdmin)
