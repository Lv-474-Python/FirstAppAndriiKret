from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TestQuiz, Questions, AnswerOption, TestQuestionUnion


# Create your views here.
def create_quiz(request):
    test_name = request.POST.get('test_name')
    test = TestQuiz.create_test_quiz(request.user, test_name=test_name)
    return render(request, 'quiz_creator.html')


def tests_list(request):
    return render(request, 'test_list.html', {
        'list': TestQuiz.objects.all()
    })


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


def add_options_to_question(request,id_question):
    current_question = Questions.objects.get(id=id_question)
    answer_amount = current_question.answers_amount

    if request.method == 'POST':
        for i in range(1, answer_amount+1):
            answer_text = request.POST.get(f'answer_text_{i}')
            is_correct = request.POST.get(f'is_correct_{i}')
            print(answer_text)

            if is_correct is None:
                is_correct = False
            else:
                is_correct = True

            answer = AnswerOption.create_answer(question=current_question, answer_text=answer_text, is_correct=is_correct)
            if i == answer_amount :
                return HttpResponse('Answers added')
    print(answer_amount)

    return render(request, 'add_answers.html', {
        'id_question': id_question,
        'answer_amount': list(range(1,answer_amount+1)),
    })