from random import shuffle

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from test_app.models import TestQuiz
from util.get_object_list_by_id import get_prepared_test, get_grade_by_user_test_id
from .models import UserAnswers
from django.http import HttpResponse


@login_required
def pass_test(request, id_test):
    """
    render list to pass with prepared and shuffled twenty questions and answers

    :param request:
    :param id_test:
    :return: render prepared list
    """
    if not UserAnswers.do_user_passed_test(request.user, id_test):
        all_questions_and_answers = get_prepared_test(id_test)
        shuffle(all_questions_and_answers)
        displayed_questions_and_answers = all_questions_and_answers[:20]

        if request.method == "POST":
            for i in displayed_questions_and_answers:
                answer_id = request.POST.get(f"{i['question'].id}")
                UserAnswers.create_user_answer_by_user_and_ids(request.user, answer_id, id_test)
            return redirect('test_result', id_test=id_test)

        return render(request, 'test_passing.html', {
            'questions_and_answers': displayed_questions_and_answers,
            'current_test': TestQuiz.get_test_by_id(id_test)
        })
    return HttpResponse('You already passed this test')


@login_required
def current_result(request, id_test):
    """
    returns render

    :param request:
    :param id_test:
    :return: {'test': contains test object,
            'mark': contains amount of correct answers,
            'max_mark': contains amount of given questions,
            'final_grade': final_grade,
            'max_final_grade': max_final_grade,
            }
    """
    if UserAnswers.do_user_passed_test(request.user, id_test):
        result = get_grade_by_user_test_id(request.user, id_test)
        return render(request, 'passed_test_result.html', result)
    return HttpResponse('You didn\'t passed test yet')


@login_required
def available_tests(request):
    available_test_list = UserAnswers.get_available_tests(request.user)
    return render(request, 'available_tests.html', {'list': available_test_list})


@login_required
def my_test_results(request):
    passed_test = UserAnswers.get_passed_test(request.user)
    results = []
    for i in passed_test:
        results.append(get_grade_by_user_test_id(request.user, i.id))
    return render(request, 'my_test_results.html', {'results': results})
