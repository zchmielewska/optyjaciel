from django.db import models


class QuestionSet(models.Model):
    question = models.CharField(max_length=256)
    option0 = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)


class Quiz(models.Model):
    year = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    question_set0 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set0")
    question_set1 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set1")
    question_set2 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set2")
    question_set3 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set3")
    question_set4 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set4")
    question_set5 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set5")
    question_set6 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set6")
    question_set7 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set7")
    question_set8 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set8")
    question_set9 = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="question_set9")


class User(models.Model):
    username = models.CharField(max_length=256)

    def __str__(self):
        return self.username


class AnswerSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer0 = models.PositiveIntegerField()
    answer1 = models.PositiveIntegerField()
    answer2 = models.PositiveIntegerField()
    answer3 = models.PositiveIntegerField()
    answer4 = models.PositiveIntegerField()
    answer5 = models.PositiveIntegerField()
    answer6 = models.PositiveIntegerField()
    answer7 = models.PositiveIntegerField()
    answer8 = models.PositiveIntegerField()
    answer9 = models.PositiveIntegerField()


class Match(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    matched_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="matched_user")
    matched_at = models.DateField(auto_now_add=True)
