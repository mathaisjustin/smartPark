"""smartPark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from . import views
from django.urls import include, re_path
# from django.conf.urls import url

urlpatterns = [
    # re_path(r'admin/', admin.site.urls),
    re_path(r'^$', views.signIn, name="index"),
    re_path(r'^postsign/', views.postsign),
    re_path(r'^logout/', views.logout, name="log"),
    re_path(r'^notification/', views.notify, name="notify"),
    re_path(r'^home/', views.home, name="home"),
    re_path(r'^feedback/', views.feedback, name="feedback"),
    re_path(r'^signup/', views.signUp, name="signup"),
    re_path(r'^postsignup/', views.postsignup, name="postsignup"),
]
