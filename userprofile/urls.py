from django.urls import path
from userprofile import views

urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='user-profile'),
    path('update_profile/<int:pk>/', views.UserProfileUpdateView.as_view(), name='update-profile')
]
