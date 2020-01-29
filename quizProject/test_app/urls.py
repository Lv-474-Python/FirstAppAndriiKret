from django.urls import path, re_path
from test_app import views

urlpatterns = [
    path('test_list', views.tests_list, name='test_list'),
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('<int:id_test>/add_question', views.add_question, name='add_question'),
    path('<int:id_question>/add_option_answer', views.add_options_to_question, name='add_option_answers')
]
