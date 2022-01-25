from django.conf import settings
from django.db import models
from django.urls import reverse


class Question(models.Model):
    question = models.CharField(max_length=256)
    option1 = models.CharField(max_length=256)
    option2 = models.CharField(max_length=256)
    option3 = models.CharField(max_length=256)
    option4 = models.CharField(max_length=256)

    def __str__(self):
        return f"[{self.id}] {self.question}"


class Quiz(models.Model):
    year = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question, through="QuizQuestion")

    class Meta:
        unique_together = ("year", "week")

    def __str__(self):
        return f"{self.year}_{self.week}"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_index = models.PositiveIntegerField()

    class Meta:
        unique_together = ("quiz", "question_index")

    def __str__(self):
        return f"{self.quiz.year}_{self.quiz.week}_{self.question_index} {self.question.question}"


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "quiz_question")


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

    def __str__(self):
        return f"{self.question} ({self.option1}, {self.option2}, {self.option3}, {self.option4}) od {self.user}"


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
    slug = models.SlugField(max_length=250, unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("game:post", args=[self.slug])
