from django.urls import path, re_path
from test_app import views

urlpatterns = [
    path('test_list', views.users_test_list, name='test_list'),
    path('my_question_list', views.my_question_list, name='my_question_list'),
    path('permanent_delete_question/<int:id_question>', views.permanent_delete_question, name='permanent_delete_question'),
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('<int:id_test>/delete', views.delete_quiz, name='delete_quiz'),
    path('delete_question_from_test/<int:id_test>/<int:id_question>', views.delete_question_from_test,
         name='delete_question_from_test'),
    re_path(r'^view_test/(?P<id_test>\w+)$', views.view_test, name='view_test'),
    re_path(r'^add_question/(?P<id_test>\w+)', views.add_question, name='add_question'),
    re_path(r'^add_existing_questions/(?P<id_test>\w+)', views.add_my_existing_questions,
            name='add_existing_questions'),
    path('<int:id_question>/add_option_answer', views.add_options_to_question, name='add_option_answers')
]
