from django.urls import path, re_path
from passing_test import views

urlpatterns = [
    path('available_test_list', views.available_tests, name='available_test_list'),
    path('my_test_results', views.my_test_results, name='my_test_results'),
    path('pass_test/<int:id_test>', views.pass_test, name='pass_test'),
    path('test_result/<int:id_test>', views.current_result, name='test_result')
]
