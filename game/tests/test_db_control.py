import random
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from game import models
from game.utils import db_control


class DbControl00Test(TestCase):
    # DB is empty

    def test_create_ten_questions(self):
        db_control.create_ten_questions()
        questions = models.Question.objects.all()
        self.assertEqual(questions.count(), 10)

    def test_get_quiz(self):
        db_control.get_quiz(year=2000, week=20)
        self.assertEqual(models.Quiz.objects.count(), 1)
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)


class DbControl01Test(TestCase):
    # DB contains 1 quiz
    fixtures = ["01.json"]

    def test_fill_quiz(self):
        quiz = models.Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 0)
        filled_quiz = db_control.fill_with_questions(quiz)
        self.assertEqual(filled_quiz.questions.count(), 10)

    def test_get_quiz(self):
        quiz = db_control.get_quiz(year=1990, week=1)
        self.assertEqual(quiz.year, 1990)
        self.assertEqual(quiz.week, 1)
        self.assertEqual(quiz.questions.count(), 10)


class DbControl02Test(TestCase):
    # DB contains 1 quiz + 2 users
    fixtures = ["02.json"]

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


class DbControl03Test(TestCase):
    # DB contains 3 quizes + 1 user who answered to 2 quizes
    fixtures = ["03.json"]

    def test_get_users_previous_quizes(self):
        user = User.objects.get(pk=1)
        previous_quizes = db_control.get_previous_quizes(user)
        self.assertEqual(len(previous_quizes), 2)

        # Quizes are sorted in chronologically (newest first)
        self.assertEqual(previous_quizes[0], models.Quiz.objects.get(pk=2))
        self.assertEqual(previous_quizes[1], models.Quiz.objects.get(pk=1))

        # Current quiz is not included in the result
        year, week, day = now().isocalendar()
        current_quiz = db_control.get_quiz(year=year, week=week)
        self.assertEqual(models.Quiz.objects.count(), 4)
        for i in range(10):
            quiz_question = current_quiz.quizquestion_set.all()[i]
            models.Answer.objects.create(user=user, quiz_question=quiz_question, answer=random.randint(1, 4))
        self.assertEqual(db_control.get_previous_quizes(user), previous_quizes)


class DbControl04Test(TestCase):
    # DB contains 2 quizes + 2 users and matches
    fixtures = ["04.json"]

    def test_get_match_context(self):
        quiz1 = models.Quiz.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        context1 = {
            "exists": True,
            "quiz": quiz1,
            "user": user1,
            "matched_user": User.objects.get(pk=2),
            "score": 3,
            "points": "punkty",
        }
        self.assertEqual(db_control.get_match_context(quiz1, user1, nest=False), context1)
        self.assertEqual(db_control.get_match_context(quiz1, user1), {"match": context1})

        quiz2 = models.Quiz.objects.get(pk=2)
        context2 = {
            "exists": False,
            "quiz": quiz2,
        }
        self.assertEqual(db_control.get_match_context(quiz2, user1, nest=False), context2)
        self.assertEqual(db_control.get_match_context(quiz2, user1), {"match": context2})


class DbControl05Test(TestCase):
    # DB contains 4 quizes + 4 users and matches
    fixtures = ["05.json"]

    def test_get_matches_queryset(self):
        user = User.objects.get(pk=1)
        quizes = models.Quiz.objects.all()
        matches_queryset = User.objects.filter(pk__in=[2, 3])
        self.assertEqual(list(db_control.get_matches_queryset(user, quizes)), list(matches_queryset))
