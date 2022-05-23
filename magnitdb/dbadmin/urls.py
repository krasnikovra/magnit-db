from django.urls import path
from . import views

app_name='dbadmin'
urlpatterns = [
    path('', views.index, name='index'),
    path('download', views.download, name='download'),
    path('export', views.export, name='export'),
    path('add/<str:model>', views.add, name='add'),
    path('add/<str:model>/save', views.add_save, name='add_save'),
    path('delete/<str:model>', views.delete, name='delete'),
    path('delete/<str:model>/save', views.delete_save, name='delete_save'),
    path('edit/<str:model>', views.edit, name='edit'),
    path('edit/<str:model>/save', views.edit_save, name='edit_save'),
    path('profile/<int:worker_id>', views.profile, name='profile'),
    path('profile/<int:worker_id>/edit', views.profile_edit, name='profile_edit'),
    path('profile/<int:worker_id>/edit/save', views.profile_edit_save, name='profile_edit_save'),
    path('profile/<int:worker_id>/assign_group', views.profile_assign_group, name='profile_assign_group'),
    path('profile/<int:worker_id>/assign_group/save', views.profile_assign_group_save, name='profile_assign_group_save'),
    path('search', views.search, name='search'),
    path('group/<int:group_id>', views.group, name='group'),
    path('group/add', views.group_add, name='group_add'),
    path('group/add/save', views.group_add_save, name='group_add_save'),
    path('group/delete', views.group_delete, name='group_delete'),
    path('group/delete/save', views.group_delete_save, name='group_delete_save'),
    path('group/edit', views.group_edit, name='group_edit'),
    path('group/edit/save', views.group_edit_save, name='group_edit_save'),
    path('changecellphone', views.changecellphone, name='changecellphone'),
    path('changecellphone/save', views.changecellphone_save, name='changecellphone_save'),
    path('login', views.login, name='login'),
    path('login/confirm', views.login_confirm, name='login_confirm'),
    path('logout', views.logout, name='logout'),
]