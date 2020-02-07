from django.db import models, IntegrityError
from account.models import CustomUser


# Create your models here.
class TestQuiz(models.Model):
    creator_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=30)

    objects = models.Manager()

    @staticmethod
    def create_test_quiz(creator_id, test_name):
        test_quiz = TestQuiz(creator_id=creator_id, test_name=test_name)
        try:
            test_quiz.save()
            return test_quiz
        except (ValueError, IntegrityError):
            return None

    def __str__(self):
        return f'{self.test_name}'

    @staticmethod
    def get_name_by_id(id_test):
        current_test = TestQuiz.objects.get(id=id_test)
        return current_test.test_name

    @staticmethod
    def delete_quiz(id_test, user_id):
        try:
            TestQuiz.objects.filter(id=id_test, creator_id=user_id).delete()
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def get_test_by_id(id_test):
        try:
            test = TestQuiz.objects.get(id=id_test)
            return test
        except TestQuiz.DoesNotExist:
            return None

    @staticmethod
    def check_author(id_test, user_id):
        try:
            TestQuiz.objects.get(id=id_test, creator_id=user_id)
            return True
        except TestQuiz.DoesNotExist:
            return False

    @staticmethod
    def exist(id_test):
        try:
            TestQuiz.objects.get(pk=id_test)
            return True
        except TestQuiz.DoesNotExist:
            return False


class Questions(models.Model):
    question_text = models.CharField(max_length=100, unique=True)
    answers_amount = models.IntegerField(default=4)
    one_correct_answer = models.BooleanField(default=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.question_text}'

    @staticmethod
    def create_question(user, question_text, answers_amount):
        question = Questions(creator=user, question_text=question_text, answers_amount=answers_amount)
        try:
            question.save()
            return question
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def get_question_by_id(id_question):
        try:
            return Questions.objects.get(id=id_question)
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def get_all_questions_by_creator_id(creator_id):
        try:
            all_questions = Questions.objects.filter(creator=creator_id)
            return all_questions
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def delete_permanently(question_id):
        try:
            Questions.objects.get(id=question_id).delete()
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def check_author(id_question, user_id):
        try:
            Questions.objects.get(id=id_question, creator_id=user_id)
            return True
        except Questions.DoesNotExist:
            return False

    def check_created_answer_amount(self):
        print(self.answeroption_set.all())
        return self.answers_amount == len(self.answeroption_set.all())


class AnswerOption(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.answer_text}'

    @staticmethod
    def create_answer(question, answer_text, is_correct):
        answer = AnswerOption(question_id=question, answer_text=answer_text, is_correct=is_correct)
        try:
            answer.save()
            return answer
        except (ValueError, IntegrityError):
            return None


class TestQuestionUnion(models.Model):
    test = models.ForeignKey(TestQuiz, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.test};{self.question}'

    @staticmethod
    def create_union(test, question):
        union = TestQuestionUnion(test=test, question=question)
        try:
            union.save()
            return union
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def delete_question_from_test(test, question):
        try:
            TestQuestionUnion.objects.get(test=test, question=question).delete()
        except (ValueError, IntegrityError):
            return None

    @staticmethod
    def do_test_have_questions(test):
        try:
            union = TestQuestionUnion.objects.filter(test=test)
            if union:
                for i in union:
                    if i.question.check_created_answer_amount():
                        return True
                return False
            return False
        except (IntegrityError, ValueError, TypeError):
            return None
