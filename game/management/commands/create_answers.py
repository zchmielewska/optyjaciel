import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from game import models
from game.utils import transform


faker = Faker("pl_PL")


class Command(BaseCommand):
    help = "Populate db with fake answers"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        count = options["count"]

        # There is a maximal number of new answers that can be added
        num_quizes = models.Quiz.objects.count()
        num_answers = models.Answer.objects.count() / 10
        num_users = User.objects.count()
        max_num_answers = num_users * num_quizes - num_answers

        count = max_num_answers if count > max_num_answers else count

        counter = 0
        while counter < count:
            random_user = random.choice(User.objects.all())
            random_quiz = random.choice(models.Quiz.objects.all())

            # User might have already answered for the randomly chosen quiz
            first_quiz_question = random_quiz.quizquestion_set.first()
            user_answered = len(models.Answer.objects.filter(user=random_user, quiz_question=first_quiz_question)) > 0
            if user_answered:
                continue

            # If user hasn't answered then let's populate answers
            for i in range(10):
                quiz_question = random_quiz.quizquestion_set.all()[i]
                models.Answer.objects.create(user=random_user, quiz_question=quiz_question, answer=random.randint(1, 2))

            # After each set of answers, there are new matches
            transform.recalculate_and_save_matches(random_quiz)
            counter += 1
