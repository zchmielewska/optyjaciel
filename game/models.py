from django.db import models


class Quiz(models.Model):
    year = models.PositiveIntegerField()
    week = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "week")


class QuestionSet(models.Model):
    question = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)
    option4 = models.CharField(max_length=256)


class QuizItem(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_set_index = models.PositiveIntegerField()  # TODO walidator dla wartosci 1-10
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("quiz", "question_set_index")


class User(models.Model):
    username = models.CharField(max_length=256)

    def __str__(self):
        return self.username


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_item = models.ForeignKey(QuizItem, on_delete=models.CASCADE)
    answer = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "quiz_item")


class Match(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    matched_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="matched_user")
    matched_at = models.DateField(auto_now_add=True)

