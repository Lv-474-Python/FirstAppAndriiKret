from django.urls import path, re_path
from account import views

urlpatterns = [
    path('', views.index),
    path('register', views.register, name='register'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('user_list', views.user_list, name='user list'),
]