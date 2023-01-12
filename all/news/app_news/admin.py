from django.contrib import admin
from app_news.models import News, Comment

# Register your models here.


class CommentsInline(admin.TabularInline):
    model = Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'active']
    list_filter = ['active']
    inlines = [CommentsInline]
    actions = ['active_true', 'active_false']

    def active_true(self, request, queryset):
        queryset.update(active=True)

    def active_false(self, request, queryset):
        queryset.update(active=False)

    active_true.short_description = 'Перевести в активный режим'
    active_false.short_description = 'Перевести в неактивный режим'


admin.site.register(News, NewsAdmin)


class CommentsAdmin(admin.ModelAdmin):
    search_fields = ['user_name']
    actions = ['del_comment']

    def del_comment(self, request, queryset):
        queryset.update(comment_text='Удалено администратором')

    del_comment.short_description = 'Удалить текст комментария'


admin.site.register(Comment, CommentsAdmin)

# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass
