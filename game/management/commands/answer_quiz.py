import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from game.models import *


class Command(BaseCommand):
    help = "Create random answers to a specific quiz by a given user"

    def add_arguments(self, parser):
        parser.add_argument('quiz_id', type=int)
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user = User.objects.get(id=options["user_id"])
        quiz = Quiz.objects.get(id=options["quiz_id"])
        for i in range(10):
            quiz_item = quiz.quizitem_set.all()[i]
            Answer.objects.create(user=user, quiz_item=quiz_item, answer=random.randint(1, 4))
