from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_lists, name="display-lists"),
    path('add_new_list/add', views.add_new_list, name="add-new-list"),
    path('<int:list_id>/add_new_task/', views.add_new_task, name="add-new-task"),
    path('<int:list_id>/delete_list/', views.delete_list, name="delete-list"),
    path('<int:list_id>/edit_list/', views.edit_list, name="edit-list"),
    path('<int:list_id>/sort/', views.sort_tasks, name="sort-tasks"),
    path('<int:list_id>/<int:task_id>/update/', views.update_task, name="update-task"),
    path('<int:list_id>/', views.display_lists, name="display-tasks"),

]
