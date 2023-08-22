from django.urls import path
from requestmanagement import views

urlpatterns = [
    path('make_request/', views.RequestManagementCreateView.as_view(), name='make-request'),
    path('requests/', views.RequestManagementListView.as_view(), name='requests-list'),
    path('request_details/<int:pk>/', views.RequestManagementDetailView.as_view(), name='request-details'),
    path('update_request/<int:pk>/', views.RequestManagementUpdateView.as_view(), name='update-request'),
    path('delete_request/<int:pk>/', views.RequestManagementDeleteView.as_view(), name='delete-request')
]
