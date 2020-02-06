from test_app.models import TestQuestionUnion, Questions, TestQuiz
from passing_test.models import UserAnswers


def get_full_test(id_test):
    """
        Returns so
        :param id_test: pk number of test object
        :return: list which includes dict with questions and Queryset of answers if or nor answers exist
        """
    union = TestQuestionUnion.objects.filter(test_id=id_test)
    questions_and_answers = []
    for i in union:
        try:
            question = Questions.objects.get(id=i.question_id)
            answer_options = question.answeroption_set.all()
            questions_and_answers.append({
                'question': question,
                'answer_options': answer_options
            })
        except Questions.DoesNotExist:
            continue
    return questions_and_answers


def get_prepared_test(id_test):
    """
    :param id_test:
    :return: list which includes dict with questions and Queryset of answers,
     but only in answers_amount field of question equal to answers object amount
    """
    full_test = get_full_test(id_test)
    prepared_test_list = []
    for i in full_test:
        if i['question'].check_created_answer_amount():
            prepared_test_list.append({
                'question': i['question'],
                'answer_options': i['answer_options']
            })
    return prepared_test_list


# TODO get grades by passing tests
def get_grade_by_user_test_id(user, id_test):
    test = TestQuiz.get_test_by_id(id_test)
    result = UserAnswers.get_test_result(user, id_test)
    correct_answers = 0
    max_correct_answer = len(result)
    max_final_grade = 300.0
    for i in result:
        a = i.chosen_answer.is_correct
        if a:
            correct_answers += 1
    final_grade = (correct_answers / max_correct_answer) * max_final_grade

    return {'test': test,
            'mark': correct_answers,
            'max_mark': max_correct_answer,
            'final_grade': final_grade,
            'max_final_grade': max_final_grade,
            }
