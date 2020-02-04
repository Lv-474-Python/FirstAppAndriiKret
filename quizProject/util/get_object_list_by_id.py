from test_app.models import TestQuestionUnion, Questions


def get_open_test(id_test):
    """
    Returns so
    :param id_test: pk number of test object
    :return: list which includes dict with questions and Queryset of answers
    """
    union = TestQuestionUnion.objects.filter(test_id=id_test)
    questions_and_answers = []
    for i in union:
        question = Questions.objects.get(id=i.question_id)
        questions_and_answers.append({
            'question': question,
            'answer_option': question.answeroption_set.all()
        })
    return questions_and_answers
