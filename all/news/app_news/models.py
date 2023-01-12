from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    content = models.TextField(verbose_name=_('content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('date create'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('date update'))
    active = models.BooleanField(default=False, verbose_name=_('active flag'))
    news_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'), blank=True, null=True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, verbose_name=_('tag'), blank=True, null=True)

    def __str__(self):
        return f'{self.name[:15]}...'

    class Meta:
        db_table = "news_table"
        ordering = ['-created_at']
        verbose_name_plural = _('news')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='authors',
                               null=True, blank=True)
    comment_text = models.TextField(verbose_name='Текст комментария')
    news = models.ForeignKey('News', null=True, on_delete=models.CASCADE, verbose_name='Новость',
                             related_name='comments')
    user_name = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        if self.author:
            return f'{self.author.username} - {self.comment_text[:15]}...'
        else:
            return f'{self.user_name} - {self.comment_text[:15]}...'

    class Meta:
        db_table = "comments_table"
        verbose_name_plural = _('comments')
        verbose_name = _('comment')


class Tag(models.Model):
    title = models.CharField(max_length=32, verbose_name='Тэг')

    def __str__(self):
        return f'{self.title}'
