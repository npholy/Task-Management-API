from django.urls import path
from . import views

urlpatterns = [
    # API URLs already exist
    # Template/UI URLs
    path('ui/tasks/', views.task_list_view, name='task-list-ui'),
    path('ui/tasks/create/', views.task_create_view, name='task-create-ui'),
    path('ui/tasks/<int:pk>/update/', views.task_update_view, name='task-update-ui'),
]
