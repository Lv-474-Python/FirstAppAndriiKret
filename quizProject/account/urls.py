from django.urls import path
from user_login_reg import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register, name='register'),
]
