from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from game import models
from game.utils import db_control


# DB is empty
class DbControl00Test(TestCase):
    def test_create_ten_questions(self):
        db_control.create_ten_questions()
        questions = models.Question.objects.all()
        self.assertEqual(questions.count(), 10)

    def test_get_quiz(self):
        db_control.get_quiz(year=2000, week=20)
        self.assertEqual(models.Quiz.objects.count(), 1)
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)


# DB contains 1 quiz
class DbControl01Test(TestCase):
    fixtures = ["01.json"]

    def test_fixture(self):
        self.assertEqual(models.Quiz.objects.count(), 1)
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 0)

    def test_fill_quiz(self):
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 0)
        filled_quiz = db_control.fill_quiz_with_questions(quiz)
        self.assertEqual(filled_quiz.questions.count(), 10)

    def test_get_quiz(self):
        quiz = db_control.get_quiz(year=1990, week=1)
        self.assertEqual(quiz.year, 1990)
        self.assertEqual(quiz.week, 1)
        self.assertEqual(quiz.questions.count(), 10)


# DB contains 1 quiz + 2 users
class DbControl02Test(TestCase):
    fixtures = ["02.json"]

    def test_fixture(self):
        self.assertEqual(models.Quiz.objects.count(), 1)
        self.assertEqual(models.Question.objects.count(), 10)
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(models.Answer.objects.count(), 20)

    def test_calculate_score(self):
        quiz = models.Quiz.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.assertEqual(db_control.calculate_score(quiz, user1, user2), 3)

    def test_get_text_answer(self):
        quiz_question1 = models.QuizQuestion.objects.get(pk=1)
        quiz_question2 = models.QuizQuestion.objects.get(pk=2)
        quiz_question3 = models.QuizQuestion.objects.get(pk=3)
        quiz_question4 = models.QuizQuestion.objects.get(pk=4)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.assertEqual(db_control.get_text_answer(quiz_question1, user1), "O1")
        self.assertEqual(db_control.get_text_answer(quiz_question2, user1), "O1")
        self.assertEqual(db_control.get_text_answer(quiz_question3, user1), "O1")
        self.assertEqual(db_control.get_text_answer(quiz_question4, user1), "O1")
        self.assertEqual(db_control.get_text_answer(quiz_question1, user2), "O1")
        self.assertEqual(db_control.get_text_answer(quiz_question2, user2), "O2")
        self.assertEqual(db_control.get_text_answer(quiz_question3, user2), "O3")
        self.assertEqual(db_control.get_text_answer(quiz_question4, user2), "O4")


# DB contains 3 quizes + 1 user who answered to 2 quizes
class DbControl03Test(TestCase):
    fixtures = ["03.json"]

    def test_fixture(self):
        self.assertEqual(models.Quiz.objects.count(), 3)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(models.QuizQuestion.objects.count(), 30)
        self.assertEqual(models.Answer.objects.count(), 20)

    def test_get_users_previous_quizes(self):
        user = User.objects.get(pk=1)
        previous_quizes = db_control.get_users_previous_quizes(user)
        self.assertEqual(len(previous_quizes), 2)
        self.assertEqual(previous_quizes[0], models.Quiz.objects.get(pk=2))
        self.assertEqual(previous_quizes[1], models.Quiz.objects.get(pk=1))

        year, week, day = now().isocalendar()
        new_quiz = db_control.get_quiz(year=year, week=week)
        self.assertEqual(models.Quiz.objects.count(), 4)
        # TODO user answers new quiz
        # it doesnt change previous quizes
