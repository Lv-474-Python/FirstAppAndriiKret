from random import shuffle

from django.shortcuts import render

from util.get_object_list_by_id import get_open_test
from test_app.models import TestQuiz


def pass_test(request, id_test):
    questions_and_answers = get_open_test(id_test)
    shuffle(questions_and_answers)
    return render(request, 'test_passing.html', {
        'questions_and_answers': questions_and_answers[:10],
        'current_test': TestQuiz.get_name_by_id(id_test)
    })


def test_list(request):
    pass
