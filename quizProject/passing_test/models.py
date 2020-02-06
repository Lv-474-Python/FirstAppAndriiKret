from django.db import models, IntegrityError
from account.models import CustomUser
from test_app.models import TestQuiz, Questions, AnswerOption, TestQuestionUnion


class UserAnswers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    test = models.ForeignKey(TestQuiz, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    chosen_answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    @staticmethod
    def create_user_answer(user, test, question, chosen_answer):
        users_choice = UserAnswers(user=user, test=test, question=question, chosen_answer=chosen_answer)
        try:
            users_choice.save()
            return users_choice
        except (IntegrityError, ValueError):
            return None

    @staticmethod
    def create_user_answer_by_user_and_ids(user, answer_id, test_id):
        try:
            current_answer = AnswerOption.objects.get(id=answer_id)
            current_question = Questions.objects.get(id=current_answer.question_id.id)
            current_test = TestQuiz.objects.get(id=test_id)
            # current_union = TestQuestionUnion.objects.get(question=current_question.id)
            # current_test = TestQuiz.objects.get(id=current_union.test.id)
            try:
                UserAnswers.objects.get(user=user, test=current_test, question=current_question)
                return print('answer already exist')
            except UserAnswers.DoesNotExist:
                users_choice = UserAnswers.create_user_answer(user, current_test, current_question, current_answer)
                return users_choice
        except (IntegrityError, ValueError, TypeError):
            return None

    @staticmethod
    def get_test_result(user, test_id):
        result_query = UserAnswers.objects.filter(user=user, test_id=test_id)
        return result_query

    @staticmethod
    def do_user_passed_test(user, test_id):
        try:
            if UserAnswers.objects.filter(user=user, test=test_id):
                return True
            return False
        except (IntegrityError, ValueError, TypeError):
            return None

    @staticmethod
    def get_available_tests(user):
        all_tests = TestQuiz.objects.all()
        available_tests = []
        for i in all_tests:
            if UserAnswers.do_user_passed_test(user, i):
                continue
            available_tests.append(i)
        return available_tests

    @staticmethod
    def get_passed_test(user):
        all_tests = TestQuiz.objects.all()
        available_tests = []
        for i in all_tests:
            if UserAnswers.do_user_passed_test(user, i):
                available_tests.append(i)
        return available_tests
