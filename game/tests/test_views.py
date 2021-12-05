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
        no_answers = models.Answer.objects.count()
        self.assertEqual(no_answers, 0)
        no_matches = models.Match.objects.count()
        self.assertEqual(no_matches, 0)

        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        quiz = db_control.get_quiz(year=1990, week=25)
        quiz_questions = quiz.quizquestion_set.order_by("question_index")
        data = {
            "csrfmiddlewaretoken": "12345",
            quiz_questions[0].id: 1, quiz_questions[1].id: 3, quiz_questions[2].id: 2, quiz_questions[3].id: 4,
            quiz_questions[4].id: 2, quiz_questions[5].id: 1, quiz_questions[6].id: 3, quiz_questions[7].id: 4,
            quiz_questions[8].id: 1, quiz_questions[9].id: 2, "quiz_id": quiz.id,
        }
        response = self.client.post("/runda/", data)
        self.assertEqual(response.status_code, 302)
        no_answers = models.Answer.objects.count()
        self.assertEqual(no_answers, 10)
        no_matches = models.Match.objects.count()
        self.assertEqual(no_matches, 1)


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

        data = {
            "question": "Favourite spell?",
            "option1": "Alohamora",
            "option2": "Expecto Patronum",
        }
        response = self.client.post("/zaproponuj-pytanie/", data)
        self.assertEqual(response.status_code, 200)


class TestCompatibility(TestCase):
    # DB contains 2 quizes + 2 users and matches
    fixtures = ["04.json"]

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/kompatybilnosc/1/1/2/")
        self.assertEqual(response.status_code, 302)

        user_a = User.objects.get(pk=1)
        self.client.force_login(user_a)
        response = self.client.get("/kompatybilnosc/1/1/2/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/kompatybilnosc/1/2/1/")
        self.assertEqual(response.status_code, 404)

        #TODO zakaz manipulowania przy quiz_id i user2_id
