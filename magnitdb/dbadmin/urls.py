from django.urls import path
from . import views

app_name='dbadmin'
urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('export/', views.export, name='export'),
]