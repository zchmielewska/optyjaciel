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
        self.assertEqual(response.url, "/zaloguj/?next=/runda/")

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


class TestCompatibility(TestCase):
    fixtures = ["04.json"]

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/kompatybilnosc/1/1/2/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/kompatybilnosc/1/1/2/")

        user_a = User.objects.get(pk=1)
        self.client.force_login(user_a)
        response = self.client.get("/kompatybilnosc/1/1/2/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/kompatybilnosc/1/2/1/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/kompatybilnosc/1/1/3/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/kompatybilnosc/999/1/2/")
        self.assertEqual(response.status_code, 404)


class TestMatches(TestCase):
    fixtures = ["04.json"]

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/optyjaciele/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/optyjaciele/")

        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.client.force_login(user1)
        response = self.client.get("/optyjaciele/")
        matches = response.context.get("matches")
        self.assertEqual(len(matches), 2)

        match1 = matches[0]
        self.assertEqual(match1.get("quiz").id, 2)
        self.assertFalse(match1.get("exists"))

        match2 = matches[1]
        self.assertEqual(match2.get("quiz").id, 1)
        self.assertTrue(match2.get("exists"))
        self.assertEqual(match2.get("user"), user1)
        self.assertEqual(match2.get("matched_user"), user2)
        self.assertEqual(match2.get("score"), 3)
        self.assertEqual(match2.get("points"), "punkty")


class TestSuggestion(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/zaproponuj-pytanie/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/zaproponuj-pytanie/")

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


class TestThanks(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/dziekuje/")
        self.assertEqual(response.status_code, 200)


class TestRegister(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/zarejestruj/")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post("/zarejestruj/", {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

        User.objects.create(username="xyz")
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post("/zarejestruj/", {"username": "xyz", "password": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/zaloguj/")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post("/zaloguj/", {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 200)

        User.objects.create_user(username="test", password="test")
        response = self.client.post("/zaloguj/", {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, 302)


class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/wyloguj/")
        self.assertEqual(response.status_code, 302)


class TestMessageInbox(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/wiadomosci/odebrane/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/wiadomosci/odebrane/")

        user1 = User.objects.create_user(username="test1", password="test1")
        self.client.force_login(user1)
        response = self.client.get("/wiadomosci/odebrane/")
        self.assertEqual(response.status_code, 200)
        messages_in = response.context.get("messages_in")
        self.assertEqual(messages_in.count(), 0)

        user2 = User.objects.create_user(username="test2", password="test2")
        models.Message.objects.create(from_user=user2, to_user=user1, title="tytuł", body="treść")
        response = self.client.get("/wiadomosci/odebrane/")
        messages_in = response.context.get("messages_in")
        self.assertEqual(messages_in.count(), 1)


class TestMessageOutbox(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/wiadomosci/wyslane/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/wiadomosci/wyslane/")

        user1 = User.objects.create_user(username="test1", password="test1")
        self.client.force_login(user1)
        response = self.client.get("/wiadomosci/wyslane/")
        self.assertEqual(response.status_code, 200)
        messages_out = response.context.get("messages_out")
        self.assertEqual(messages_out.count(), 0)

        user2 = User.objects.create_user(username="test2", password="test2")
        models.Message.objects.create(from_user=user1, to_user=user2, title="tytuł", body="treść")
        response = self.client.get("/wiadomosci/wyslane/")
        messages_out = response.context.get("messages_out")
        self.assertEqual(messages_out.count(), 1)


class TestMessageWrite(TestCase):
    fixtures = ["04.json"]

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/wiadomosci/utworz/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/zaloguj/?next=/wiadomosci/utworz/")

        user_a = User.objects.get(pk=1)
        user_b = User.objects.get(pk=2)
        self.client.force_login(user_a)
        response = self.client.get("/wiadomosci/utworz/")
        self.assertEqual(response.status_code, 200)
        to_user = response.context.get("form").fields["to_user"].queryset
        self.assertEqual(to_user.count(), 1)
        self.assertEqual(to_user.first(), user_b)

        response = self.client.get("/wiadomosci/utworz/2/")
        self.assertEqual(response.status_code, 200)
        to_user = response.context.get("form").fields["to_user"].queryset
        self.assertEqual(to_user.count(), 1)
        self.assertEqual(to_user.first(), user_b)

        response = self.client.get("/wiadomosci/utworz/999/")
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        user_a = User.objects.get(pk=1)
        user_b = User.objects.get(pk=2)
        self.client.force_login(user_a)
        self.assertEqual(models.Message.objects.count(), 0)
        data = {
            "to_user": user_b.id,
            "title": "tytuł",
            "body": "treść"
        }
        response = self.client.post("/wiadomosci/utworz/", data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Message.objects.count(), 1)


class TestMessageRead(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        user1 = User.objects.create_user(username="test1", password="test1")
        self.client.force_login(user1)
        self.assertEqual(models.Message.objects.count(), 0)
        response = self.client.get("/wiadomosci/czytaj/1/")
        self.assertEqual(response.status_code, 404)

        user2 = User.objects.create_user(username="test2", password="test2")
        msg1 = models.Message.objects.create(
            from_user=user1,
            to_user=user2,
            title="tytuł1",
            body="treść1",
        )
        self.assertTrue(msg1.new)
        self.assertEqual(models.Message.objects.count(), 1)
        response = self.client.get(f"/wiadomosci/czytaj/{msg1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("msg_type"), "out")
        self.assertTrue(msg1.new)

        msg2 = models.Message.objects.create(
            from_user=user2,
            to_user=user1,
            title="tytuł2",
            body="treść2",
        )
        self.assertTrue(msg2.new)
        self.assertEqual(models.Message.objects.count(), 2)
        response = self.client.get(f"/wiadomosci/czytaj/{msg2.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("msg_type"), "in")
        self.assertFalse(models.Message.objects.get(id=msg2.id).new)


class TestBlog(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)


class TestPost(TestCase):
    fixtures = ["06.json"]

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get("/blog/ddd")
        self.assertEqual(response.status_code, 200)

