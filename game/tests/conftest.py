import pytest
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
    pass
