from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect

from util.get_object_list_by_id import get_full_test
from .models import TestQuiz, Questions, AnswerOption, TestQuestionUnion


@login_required
def users_test_list(request):
    users_tests = TestQuiz.objects.filter(creator_id=request.user.id)
    return render(request, 'test_list.html', {'list': users_tests})


@login_required
def create_quiz(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        test = TestQuiz.create_test_quiz(request.user, test_name=test_name)
        if test:
            return redirect('test_list')
    return render(request, 'quiz_creator.html')


@login_required
def delete_quiz(request, id_test):
    if TestQuiz.check_author(id_test, request.user):
        user_id = request.user.id
        TestQuiz.delete_quiz(id_test, user_id)
        return redirect('test_list')
    raise PermissionDenied()


@login_required()
def view_test(request, id_test):
    if TestQuiz.check_author(id_test, request.user):
        questions_and_answers = get_full_test(id_test)
        return render(request, 'view_test.html', {
            'questions_and_answers': questions_and_answers,
            'current_test': TestQuiz.get_test_by_id(id_test)
        })
    raise PermissionDenied()


@login_required
def add_question(request, id_test):
    if TestQuiz.exist(id_test):
        current_test = TestQuiz.get_test_by_id(id_test)
        if TestQuiz.check_author(current_test.id, request.user):
            if request.method == "POST":
                question_text = request.POST.get('question_text')
                answers_amount = request.POST.get('answers_amount')
                try:
                    question = Questions.create_question(request.user,
                                                         question_text,
                                                         answers_amount)
                    union = TestQuestionUnion.create_union(current_test, question)
                    if union:
                        return redirect('add_option_answers', id_question=question.id)
                except AttributeError:
                    error = True
                    return render(request, 'add_question.html', {'error': error, 'current_test': current_test})
            return render(request, 'add_question.html', {'current_test': current_test})
        raise PermissionDenied()
    return Http404


@login_required
def add_options_to_question(request, id_question):
    if Questions.check_author(id_question, request.user):
        current_question = Questions.get_question_by_id(id_question)
        if current_question.check_created_answer_amount():
            return redirect('test_list')
        answer_amount = current_question.answers_amount
        if request.method == 'POST':
            for i in range(answer_amount):
                answer_text = request.POST.get(f'answer_text_{i}')
                is_correct = request.POST.get('is_correct')
                is_correct = is_correct == f'{i}'
                AnswerOption.create_answer(question=current_question,
                                           answer_text=answer_text,
                                           is_correct=is_correct)
            return redirect('test_list')
        return render(request, 'add_answers.html', {
            'current_question': current_question,
            'answer_amount': list(range(answer_amount)),
        })
    raise PermissionDenied()


@login_required
def add_my_existing_questions(request, id_test):
    if TestQuiz.check_author(id_test, request.user):
        all_my_questions = Questions.objects.filter(creator=request.user)
        available = set()
        for i in all_my_questions:
            if not TestQuestionUnion.objects.filter(test=id_test, question=i):
                available.add(i)
        if available:
            if request.method == 'POST':
                selected_question = request.POST.get('selected_question')
                question = Questions.objects.get(question_text=selected_question)
                print(question)
                new_union = TestQuestionUnion.create_union(test=TestQuiz.objects.get(id=id_test), question=question)
                if new_union:
                    return redirect('view_test', id_test=id_test)
            return render(request, 'add_existing_questions.html', {'questions': available, 'no_questions': False})
        return render(request, 'add_existing_questions.html', {'questions': available, 'no_questions': True})
    raise PermissionDenied()


@login_required
def delete_question_from_test(request, id_test, id_question):
    if TestQuiz.check_author(id_test, request.user):
        if Questions.check_author(id_question, request.user):
            TestQuestionUnion.delete_question_from_test(id_test, id_question)
            return redirect('view_test', id_test=id_test)
        raise PermissionDenied()
    raise PermissionDenied()


@login_required
def my_question_list(request):
    questions = Questions.get_all_questions_by_creator_id(request.user)
    questions_and_answers = []
    for i in questions:
        answer_options = i.answeroption_set.all()
        questions_and_answers.append(
            {
                'question': i,
                'answer_options': answer_options
            }
        )

    return render(request, 'my_question_list.html', {'questions_and_answers': questions_and_answers})


@login_required
def permanent_delete_question(request, id_question):
    if Questions.check_author(id_question, request.user):
        Questions.delete_permanently(id_question)
        return redirect('my_question_list')
    raise PermissionDenied()
