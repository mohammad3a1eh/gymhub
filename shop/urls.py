from django.urls import path
from . import views

urlpatterns = [
    path('create-request/', views.create_request, name='create_request'),
    path('upload-program/<int:request_id>/', views.upload_program, name='upload_program'),
    path('download/<int:request_id>/', views.secure_file_download, name='secure_file_download'),
]
