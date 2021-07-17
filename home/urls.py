"""Blog URL Configuration

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
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.index, name="index"),
    path('blogs/', views.blog, name="blogs"),
    path('blog/<int:id>', views.post, name="blog"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('forgot_password', views.forgot_pass, name="forgot_password"),
    path('reset_password', views.reset_pass, name="reset_password"),
    path('search', views.search, name="search"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/profile', views.dashboard_profile, name="dashboard/profile"),
    path('dashboard/change_pass', views.change_pass, name="dashboard/change_pass"),
    path('dashboard/blogs', views.dashboard_blogs, name="dashboard/blogs"),
    path('dashboard/edit_blog/<int:id>', views.edit_blog, name="dashboard/edit_blog"),
    path('dashboard/delete_blog/<int:id>', views.delete_blog, name="dashboard/delete_blog"),
    path('dashboard/add_blog', views.dashboard_addblog, name="dashboard/add_blog"),
]
