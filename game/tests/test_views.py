import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.timezone import now

from game import models
from game.utils import db_control


class TestRules(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestGame(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/runda/")
        self.assertEqual(response.status_code, 302)

        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        response = self.client.get("/runda/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("quiz_questions")), 10)

        year, week, day = now().isocalendar()
        quiz = response.context.get("quiz")
        self.assertEqual(quiz.year, year)
        self.assertEqual(quiz.week, week)

    def test_post(self):
        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        quiz = db_control.get_quiz(year=1990, week=25)
        quiz_questions = quiz.quizquestion_set.order_by("question_index")
        data = {
            "csrfmiddlewaretoken": "12345",
            quiz_questions[0].id: 1,
            quiz_questions[1].id: 3,
            quiz_questions[2].id: 2,
            quiz_questions[3].id: 4,
            quiz_questions[4].id: 2,
            quiz_questions[5].id: 1,
            quiz_questions[6].id: 3,
            quiz_questions[7].id: 4,
            quiz_questions[8].id: 1,
            quiz_questions[9].id: 2,
            "quiz_id": quiz.id,
        }
        response = self.client.post("/runda/", data)
        self.assertEqual(response.status_code, 302)

    def test_post_answer_is_not_between_one_and_four(self):
        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        quiz = db_control.get_quiz(year=1990, week=25)
        quiz_questions = quiz.quizquestion_set.order_by("question_index")
        data = {
            "csrfmiddlewaretoken": "12345",
            quiz_questions[0].id: 5,
            quiz_questions[1].id: 1,
            quiz_questions[2].id: 1,
            quiz_questions[3].id: 1,
            quiz_questions[4].id: 1,
            quiz_questions[5].id: 1,
            quiz_questions[6].id: 1,
            quiz_questions[7].id: 1,
            quiz_questions[8].id: 1,
            quiz_questions[9].id: 1,
            "quiz_id": quiz.id,
        }
        response = self.client.post("/runda/", data)
        self.assertEqual(response.status_code, 302)


class TestSuggestion(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/zaproponuj-pytanie/")
        self.assertEqual(response.status_code, 302)

        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        response = self.client.get("/zaproponuj-pytanie/")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        data = {
            "question": "Favourite spell?",
            "option1": "Alohamora",
            "option2": "Expecto Patronum",
            "option3": "Avada Kedavra",
            "option4": "Lumos",
        }
        response = self.client.post("/zaproponuj-pytanie/", data)
        self.assertEqual(response.status_code, 302)

    def test_post_incomplete_query_returns_back_to_form(self):
        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        data = {
            "question": "Favourite spell?",
            "option1": "Alohamora",
            "option2": "Expecto Patronum",
        }
        response = self.client.post("/zaproponuj-pytanie/", data)
        self.assertEqual(response.status_code, 200)
