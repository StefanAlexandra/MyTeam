from django.urls import path
from project import views

urlpatterns = [
    path('add_project/', views.ProjectCreateView.as_view(), name='add-project'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('update_project/<int:pk>', views.ProjectUpdateView.as_view(), name='update-project'),
    path('project_details/<int:pk>', views.ProjectDetailView.as_view(), name='project-details'),
    path('delete_project/<int:pk>', views.ProjectDeleteView.as_view(), name='delete-project')
]
