from django.urls import path

from .views import AuthorsList, BooksList, AuthorDetail, BookDetail


urlpatterns = [
    path('authors/', AuthorsList.as_view(), name='authors-list'),
    path('books/', BooksList.as_view(), name='books-list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail')
]
