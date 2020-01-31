from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TestQuiz, Questions, AnswerOption, TestQuestionUnion


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
    TestQuiz.objects.filter(id=id_test, creator_id=request.user.id).delete()
    return redirect('test_list')


@login_required()
def view_test(request, id_test):
    current_test = TestQuiz.objects.get(id=id_test)
    union = TestQuestionUnion.objects.filter(test_id=id_test)
    print(union)
    q_a = []
    for i in union:
        q = Questions.objects.get(id=i.question_id)
        q_a.append({
            'q': q,
            'ao': q.answeroption_set.all()
        })
    print(q_a)
    return render(request, 'view_text.html', {'q_a': q_a, 'current_test': current_test})


@login_required
def add_question(request, id_test):
    current_test = TestQuiz.objects.get(pk=id_test)

    if request.method == "POST":
        question_text = request.POST.get('question_text')
        answers_amount = request.POST.get('answers_amount')
        one_correct_answer = request.POST.get('one_correct_answer')
        question = Questions.create_question(question_text, answers_amount, one_correct_answer)
        union = TestQuestionUnion.create_union(current_test, question)

        if union:
            return redirect('add_option_answers', id_question=question.id)

    return render(request, 'add_question.html')


@login_required
def add_options_to_question(request, id_question):
    current_question = Questions.objects.get(id=id_question)
    answer_amount = current_question.answers_amount

    if request.method == 'POST':
        for i in range(1, answer_amount + 1):
            answer_text = request.POST.get(f'answer_text_{i}')
            is_correct = request.POST.get(f'is_correct')
            print(is_correct)

            if is_correct == f'{i}':
                is_correct = True
            else:
                is_correct = False

            AnswerOption.create_answer(question=current_question, answer_text=answer_text,
                                       is_correct=is_correct)
            if i == answer_amount:
                return redirect('test_list')
    print(answer_amount)

    return render(request, 'add_answers.html', {
        'id_question': id_question,
        'answer_amount': list(range(1, answer_amount + 1)),
    })
