from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect

from util.get_object_list_by_id import get_full_test
from .models import TestQuiz, Questions, AnswerOption, TestQuestionUnion

# TODO create opportunity to add created questions
@login_required
def tests_list(request):
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
    user_id = request.user.id
    TestQuiz.delete_quiz(id_test, user_id)
    return redirect('test_list')


@login_required()
def view_test(request, id_test):
    questions_and_answers = get_full_test(id_test)
    return render(request, 'view_test.html', {
        'questions_and_answers': questions_and_answers,
        'current_test': TestQuiz.get_name_by_id(id_test)
    })


@login_required
def add_question(request, id_test):
    try:
        current_test = TestQuiz.objects.get(pk=id_test)
    except TestQuiz.DoesNotExist:
        raise Http404('Such test don\'t exist')
    if current_test.creator_id == request.user:
        if request.method == "POST":
            question_text = request.POST.get('question_text')
            answers_amount = request.POST.get('answers_amount')
            # one_correct_answer = request.POST.get('one_correct_answer')
            try:
                question = Questions.create_question(question_text, answers_amount, True)  # , one_correct_answer)
                union = TestQuestionUnion.create_union(current_test, question)
                if union:
                    return redirect('add_option_answers', id_question=question.id)
            except AttributeError:
                error = True
                return render(request, 'add_question.html', {'error': error})

        return render(request, 'add_question.html')
    raise PermissionDenied()


@login_required
def add_options_to_question(request, id_question):
    current_question = Questions.objects.get(id=id_question)
    # print(current_question.check_created_answer_amount())
    if current_question.check_created_answer_amount():
        return redirect('test_list')
    answer_amount = current_question.answers_amount

    if request.method == 'POST':

        for i in range(1, answer_amount + 1):
            answer_text = request.POST.get(f'answer_text_{i}')
            is_correct = request.POST.get('is_correct')
            is_correct = is_correct == f'{i}'

            AnswerOption.create_answer(question=current_question, answer_text=answer_text,
                                       is_correct=is_correct)
            if i == answer_amount:
                return redirect('test_list')
    print(answer_amount)

    return render(request, 'add_answers.html', {
        'id_question': id_question,
        'answer_amount': list(range(1, answer_amount + 1)),
    })

# def _get_test(id_test):
#     # current_test = TestQuiz.objects.get(id=id_test)
#     union = TestQuestionUnion.objects.filter(test_id=id_test)
#     questions_and_answers = []
#     for i in union:
#         question = Questions.objects.get(id=i.question_id)
#         questions_and_answers.append({
#             'question': question,
#             'answer_option': question.answeroption_set.all()
#         })
#     return questions_and_answers
