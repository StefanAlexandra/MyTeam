from django.urls import path
from userextend import views

urlpatterns =[
    path('manager_sign_up/', views.ManagerSignUpView.as_view(), name='manager-sign-up')

]
