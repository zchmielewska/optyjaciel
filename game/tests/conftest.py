import pytest
from django.contrib.auth.models import User
from django.utils.timezone import now
from faker import Faker

from game import models
from game.utils import db_control

faker = Faker("pl_PL")


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
def quiz_with_questions(questions):
    quiz = models.Quiz.objects.create(year=1995, week=10)
    quiz = db_control.fill_quiz_with_questions(quiz)
    return quiz


@pytest.fixture()
def user():
    user = User.objects.create(username=faker.profile()["username"], password=faker.password())
    return user


@pytest.fixture()
def answers(quiz_with_questions, user):
    answers = []
    for i in range(10):
        quiz_question = quiz_with_questions.quizquestion_set.all()[i]
        answer = models.Answer.objects.create(user=user, quiz_question=quiz_question, answer=random.randint(1, 4))
        answers.append(answer)
    return answers
