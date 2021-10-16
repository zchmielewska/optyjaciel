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
    QuestionSet0 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet0")
    QuestionSet1 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet1")
    QuestionSet2 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet2")
    QuestionSet3 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet3")
    QuestionSet4 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet4")
    QuestionSet5 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet5")
    QuestionSet6 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet6")
    QuestionSet7 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet7")
    QuestionSet8 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet8")
    QuestionSet9 = models.ForeignKey(QuestionSet, on_delete=models.PROTECT, related_name="QuestionSet9")

