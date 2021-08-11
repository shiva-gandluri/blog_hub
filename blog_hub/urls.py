"""blog_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from django.contrib.auth import views
from blog import views as custom_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('blog.urls')),
    url('accounts/login/', views.LoginView.as_view(), name='login'),
    url('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout', kwargs={}),
    path('register/', custom_views.RegisterPage.as_view(), name='register'),
]
