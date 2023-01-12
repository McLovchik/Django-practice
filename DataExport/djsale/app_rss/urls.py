from django.urls import path
from .feeds import LatestNewsFeed

urlpatterns = [
    path('latest/feed/', LatestNewsFeed()),
]
