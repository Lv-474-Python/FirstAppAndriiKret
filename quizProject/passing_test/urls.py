from django.urls import path, re_path
from passing_test import views

urlpatterns = [
    path('tests', views.test_list, name='available_test_list'),
    path('pass_test/<int:id_test>', views.pass_test, name='pass_test'),
]
