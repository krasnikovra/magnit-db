from django.urls import path
from . import views

app_name='dbadmin'
urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('export/', views.export, name='export'),
    path('add/<str:model>', views.add, name='add'),
    path('add/<str:model>/save', views.add_save, name='add_save'),
    path('delete/<str:model>', views.delete, name='delete'),
    path('delete/<str:model>/save', views.delete_save, name='delete_save'),
]