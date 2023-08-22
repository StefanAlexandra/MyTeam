from django.urls import path
from member import views

urlpatterns = [
    path('add_member/', views.MemberSignUpView.as_view(), name='add-member'),
    path('members/', views.MemberListView.as_view(), name='members'),
    path('member_profile/<int:pk>/', views.MemberDetailView.as_view(), name='member-profile'),
    path('update_member_profile/<int:pk>/', views.MemberUpdateView.as_view(), name='update-member-profile'),
    path('delete_member/<int:pk>/', views.MemberDeleteView.as_view(), name='delete-member')
]
