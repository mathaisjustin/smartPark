from django.urls import path
from .views import upload_feedback, home_redirect

urlpatterns = [
    path('',upload_feedback, name = "feedback" ),
    path('home/',home_redirect ),
]