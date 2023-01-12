from django.urls import path
from .views import upload_file, model_form_upload, upload_files


urlpatterns = [
    path('upload_file/', upload_file, name='upload-file'),
    path('model_form_upload_file/', model_form_upload, name='model-form-upload-file'),
    path('upload_files/', upload_files, name='upload-files')
]
