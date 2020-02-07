from django.urls import path, re_path
from account import views

urlpatterns = [
    path('', views.index, ''),
    path('home_page', views.index, name='home_page'),
    path('register_user', views.register, name='register_user'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
]
