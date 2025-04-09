from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_converter_view, name='upload'),
    path('ajax-upload/', views.ajax_upload, name='ajax_upload'), 
]
