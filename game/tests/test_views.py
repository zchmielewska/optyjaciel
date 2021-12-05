import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.timezone import now


class TestRules(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client(self):
        response = self.client.get("/")
        assert response.status_code == 200


class TestGame(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client(self):
        response = self.client.get("/runda/")
        assert response.status_code == 302

        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        response = self.client.get("/runda/")
        assert response.status_code == 200
        assert len(response.context.get("quiz_questions")) == 10

        year, week, day = now().isocalendar()
        quiz = response.context.get("quiz")
        assert quiz.year == year
        assert quiz.week == week


class TestSuggestion(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client(self):
        response = self.client.get("/zaproponuj-pytanie/")
        assert response.status_code == 302

        user = User.objects.create(username='testuser')
        self.client.force_login(user)
        response = self.client.get("/zaproponuj-pytanie/")
        assert response.status_code == 200
