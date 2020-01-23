from django.urls import path
from account import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register, name='register'),
]
