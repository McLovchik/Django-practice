from django.contrib import admin
from .models import Author, Book


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)


class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)

