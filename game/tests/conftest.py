import pytest
from django.contrib.auth.models import User
from django.utils.timezone import now

from game import models


@pytest.fixture()
def questions(count=10):
    questions = []
    for i in range(count):
        question = models.Question.objects.create(
            question=f"Pytanie {i}",
            option1=f"Opcja 1 {i}",
            option2=f"Opcja 2 {i}",
            option3=f"Opcja 3 {i}",
            option4=f"Opcja 4 {i}",
        )
        questions.append(question)
    return questions


@pytest.fixture()
def current_quiz():
    year, week, day = now().isocalendar()
    quiz = models.Quiz.objects.create(year=year, week=week)
    return quiz


@pytest.fixture()
def users(count=1):
    users = []
    for _ in range(count):
        user = User.objects.create(username="jankowalski", password="1234")
        users.append(user)
    return users


@pytest.fixture()
def answers(current_quiz, users):
    answers = []
    for i in range(10):
        quiz_question = quiz.quizquestion_set.all()[i]
        answer = models.Answer.objects.create(user=user, quiz_question=quiz_question, answer=random.randint(1, 4))
        answers.append(answer)
    return answers
