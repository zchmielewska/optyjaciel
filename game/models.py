from django.conf import settings
from django.db import models


class Quiz(models.Model):
    year = models.PositiveIntegerField()
    week = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "week")

    def __str__(self):
        return f"{self.year}_{self.week}"


class QuestionSet(models.Model):
    question = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)
    option4 = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.question} (1: {self.option1}, 2: {self.option2}, 3: {self.option3}, 4: {self.option4})"


class QuizItem(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_set_index = models.PositiveIntegerField()  # TODO walidator dla wartosci 1-10
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("quiz", "question_set_index")


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz_item = models.ForeignKey(QuizItem, on_delete=models.CASCADE)
    answer = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "quiz_item")


class Match(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    matched_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="matched_user")
    matched_at = models.DateTimeField(auto_now_add=True)


class Suggestion(models.Model):
    question = models.CharField(max_length=256, verbose_name="pytanie")
    option1 = models.CharField(max_length=256, verbose_name="Odpowiedź 1")
    option2 = models.CharField(max_length=256, verbose_name="Odpowiedź 2")
    option3 = models.CharField(max_length=256, verbose_name="Odpowiedź 3")
    option4 = models.CharField(max_length=256, verbose_name="Odpowiedź 4")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    suggested_at = models.DateTimeField(auto_now_add=True)
