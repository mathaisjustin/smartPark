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
from django.urls import path, include
# from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payment.urls')),
    path('feedback/', include('feedback.urls')),
    path('', views.signIn, name="index"),
    path('logout/', views.logout, name="log"),
    path('postsign/', views.postsign),
    path('notification/', views.notify, name="notify"),
    path('home/', views.home, name="home"),
    path('userdetails/', views.userdetails),
    path('postuserdetails/', views.postuserdetails),
    path('profile/', views.profile, name="profile"),
    path('postprofile/', views.postprofile, name="postprofile"),
    # path('feedback/', views.feedback, name="feedback"),
    path('signup/', views.signUp, name="signup"),
    path('postsignup/', views.postsignup, name="postsignup"),
    path('subscription/', views.subscription),
    path('postsubscription/', views.subscription, name="postsubscription"),
    path('paymentsuccess/', views.successpayment),
    path('terms/', views.terms, name="terms"),
]
