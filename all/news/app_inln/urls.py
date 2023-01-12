from django.urls import path
from .views import inln_page_view

urlpatterns = [
        path('', inln_page_view, name='inln-page')
]
