from django.urls import path
from .views import get_news_in_custom_format, NewsItemDetailView, NewsListView


urlpatterns = [
    path('', get_news_in_custom_format, name='news-list'),
    path('<int:pk>/', NewsItemDetailView.as_view(), name='news-item'),
    path('news/', NewsListView.as_view(), name='news_list'),
]
