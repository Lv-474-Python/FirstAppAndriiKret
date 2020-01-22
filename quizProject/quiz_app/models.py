from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    rank = models.IntegerField()


class Test(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    test_name = models.CharField(max_length=50)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL)


class QuizAnswer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
