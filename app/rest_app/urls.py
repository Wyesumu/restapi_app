from django.urls import path

from . import views

urlpatterns = [
    path('top', views.GetData.as_view(), name='top'),
    path('upload', views.UploadData.as_view(), name='upload'),
]
