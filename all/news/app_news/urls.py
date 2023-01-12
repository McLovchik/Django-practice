from django.urls import path
from .views import NewsFormView, NewsEditFormView, NewsListView, NewsCommentsPageView, activate_news_view, NewsFilterTag

urlpatterns = [
    path('create/', NewsFormView.as_view(), name='news-create'),
    path('edit/<int:news_id>/', NewsEditFormView.as_view(), name='news-edit'),
    path('', NewsListView.as_view(), name='new-list-url'),
    path('<int:pk>/', NewsCommentsPageView.as_view(), name='news-comments-page'),
    path('activate_news/<int:pk>/', activate_news_view, name='activate-news'),
    path('<str:news_tag>', NewsFilterTag.as_view(), name='news-with-tag')
]
