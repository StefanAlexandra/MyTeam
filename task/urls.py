from django.urls import path

from task import views

urlpatterns = [
    path('assign_task/', views.TaskCreateView.as_view(), name='assign-task'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task_details/<int:pk>/', views.TaskDetailView.as_view(), name='task-details'),
    path('update_task/<int:pk>/', views.TaskUpdateView.as_view(), name='update-task'),
    path('delete_task/<int:pk>/', views.TaskDeleteView.as_view(), name='delete-task')
]
