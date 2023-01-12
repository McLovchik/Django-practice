from django.contrib import admin
from .models import Record


class RecordsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Record, RecordsAdmin)
