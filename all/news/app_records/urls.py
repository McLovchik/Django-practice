from django.urls import path
from .views import create_record, RecordsListView, RecordDetailView, create_record_csv
# from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', RecordsListView.as_view(), name='records-list'),
    path('create/', create_record, name='create-record'),
    # path('create/', cache_page(30)(create_record), name='create-record'),
    path('<int:pk>', RecordDetailView.as_view(), name='record-detail'),
    path('create_csv/', create_record_csv, name='create-csv'),
]
