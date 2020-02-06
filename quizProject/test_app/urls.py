from django.urls import path, re_path
from test_app import views

urlpatterns = [
    path('test_list', views.tests_list, name='test_list'),
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('<int:id_test>/delete', views.delete_quiz, name='delete_quiz'),
    re_path(r'^view_test/(?P<id_test>\w+)$', views.view_test, name='view_test'),
    re_path(r'^add_question/(?P<id_test>\w+)', views.add_question, name='add_question'),
    path('<int:id_question>/add_option_answer', views.add_options_to_question, name='add_option_answers')
]
