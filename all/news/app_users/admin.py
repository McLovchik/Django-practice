from django.contrib import admin
from .models import Profile, PersonalCabinet


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', )


admin.site.register(Profile, ProfileAdmin)


class PersonalCabinetAdmin(admin.ModelAdmin):
    list_display = ('profile', )


admin.site.register(PersonalCabinet, PersonalCabinetAdmin)
