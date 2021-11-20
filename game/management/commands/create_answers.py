import random
import game.utils.transform
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from game.models import *


faker = Faker("pl_PL")


class Command(BaseCommand):
    help = "Populate db with fake answers"

    def add_arguments(self, parser):
        parser.add_argument("answers_count", type=int)

    def handle(self, *args, **options):
        count = options["answers_count"]

        # There is a maximal number of new answers that can be added
        no_of_quizes = Quiz.objects.count()
        no_of_answers = Answer.objects.count() / 10
        no_of_users = User.objects.count()
        max_no_of_new_answers = no_of_users * no_of_quizes - no_of_answers

        count = max_no_of_new_answers if count > max_no_of_new_answers else count

        counter = 0
        while counter < count:
            random_user = random.choice(User.objects.all())
            random_quiz = random.choice(Quiz.objects.all())

            # User might have already answered for the randomly chosen quiz
            first_quiz_question = random_quiz.quizquestion_set.first()
            user_answered = len(Answer.objects.filter(user=random_user, quiz_question=first_quiz_question)) > 0
            if user_answered:
                continue

            # If user hasn't answered then let's populate answers
            for i in range(10):
                quiz_question = random_quiz.quizquestion_set.all()[i]
                Answer.objects.create(user=random_user, quiz_question=quiz_question, answer=random.randint(1, 4))

            # After each set of answers, there are new matches
            game.utils.transform.recalculate_and_save_matches(random_quiz)
            counter += 1
