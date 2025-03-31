from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)
    option4 = models.CharField(max_length=256)


class Quiz(models.Model):
    date = models.CharField(max_length=8)
    questions = models.ManyToManyField(Question, through="QuizQuestion")


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_index = models.PositiveIntegerField()


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.PositiveIntegerField()


class Match(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    matched_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="matched_user")
    matched_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="to_user")
    sent_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1024)
    body = models.TextField()
    new = models.BooleanField(default=True)


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    slug = models.SlugField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)