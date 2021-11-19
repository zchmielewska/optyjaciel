import random
import game.utils.transform
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from game.models import *


faker = Faker("pl_PL")


class Command(BaseCommand):
    help = "Populate db with fake data"

    def handle(self, *args, **options):
        self.create_fake_users()
        self.create_fake_answers(10)

    @staticmethod
    def create_fake_users(count=1):
        for _ in range(count):
            username = faker.profile()["username"]
            password = faker.password()
            User.objects.create_user(username=username, password=password)

    @staticmethod
    def create_fake_answers(count=1):
        # There is a maximal number of new answers to be added
        no_of_quizes = Quiz.objects.count()
        no_of_answers = Answer.objects.count() / 10
        no_of_users = User.objects.count()
        max_no_of_new_answers = no_of_users * no_of_quizes - no_of_answers
        count = max_no_of_new_answers if count > max_no_of_new_answers else count

        counter = 0
        while counter <= count:
            random_user = random.choice(User.objects.all())
            random_quiz = random.choice(Quiz.objects.all())

            first_quiz_item = random_quiz.quizitem_set.first()
            user_answered = len(Answer.objects.filter(user=random_user, quiz_item=first_quiz_item)) > 0
            if user_answered:
                continue

            for i in range(10):
                quiz_item = random_quiz.quizitem_set.all()[i]
                Answer.objects.create(user=random_user, quiz_item=quiz_item, answer=random.randint(1, 4))

            # After each set of answers, there are new matches
            game.utils.transform.recalculate_and_save_matches(random_quiz)
            counter += 1
