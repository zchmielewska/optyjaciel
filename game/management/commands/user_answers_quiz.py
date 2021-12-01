import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from game import models


class Command(BaseCommand):
    help = "Create random answers to a specific quiz by a given user"

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('quiz_id', type=int)

    def handle(self, *args, **options):
        user = User.objects.get(id=options["user_id"])
        quiz = models.Quiz.objects.get(id=options["quiz_id"])
        for i in range(10):
            quiz_question = quiz.quizquestion_set.all()[i]
            models.Answer.objects.create(user=user, quiz_question=quiz_question, answer=random.randint(1, 4))
