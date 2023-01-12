from django.urls import path
from .views import About, Contacts, HousingObjectListView, HousingObjectDetailView

urlpatterns = [
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('real_estate_list/', HousingObjectListView.as_view(), name='main'),
    path('<int:pk>/real_estate_detail/', HousingObjectDetailView.as_view(), name='real_estate_detail')
]
