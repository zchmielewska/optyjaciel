from django.utils.timezone import now
import datetime
import numpy as np
import pandas as pd
import pytest

from game import models


@pytest.mark.django_db
def test_create_ten_questions():
    assert models.Question.objects.count() == 0
    utils.create_ten_questions()
    assert models.Question.objects.count() == 10


@pytest.mark.django_db
def test_get_or_create_quiz_gets_current_quiz_if_exists(current_quiz):
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 1
    quiz = utils.get_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_current_quiz_from_existing_questions(questions):
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_quiz_for_specific_week_from_existing_questions(questions):
    year = 2000
    week = 1
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_quiz(year=year, week=week)
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_current_quiz_even_if_there_are_no_questions():
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_quiz_for_specific_week_even_if_there_are_no_questions():
    year = 2000
    week = 1
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_quiz(year=year, week=week)
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week
