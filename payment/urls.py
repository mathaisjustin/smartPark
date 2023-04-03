from django.urls import path
from .views import home, success
from .import views

urlpatterns = [
    path('', views.home),
    path('success/', views.success),
]
