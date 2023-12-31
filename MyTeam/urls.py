"""
URL configuration for MyTeam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.views.generic import RedirectView

from userextend.forms import AuthenticationNewForm, PasswordChangeNewForm, PasswordResetNewForm, SetPasswordNewForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login/', views.LoginView.as_view(form_class=AuthenticationNewForm), name='login'),
    path('password_change/', views.PasswordChangeView.as_view(form_class=PasswordChangeNewForm), name='password-change-form'),
    path('password_reset/', views.PasswordResetView.as_view(form_class=PasswordResetNewForm), name='password-reset-form'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(form_class=SetPasswordNewForm), name='password-confirm-form'),
    path('', include('django.contrib.auth.urls')),
    path('', include('userextend.urls')),
    path('', include('member.urls')),
    path('', include('userprofile.urls')),
    path('', include('project.urls')),
    path('', include('task.urls')),
    path('', include('requestmanagement.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
