from django.utils.timezone import now
import datetime
import pytest

from game.utils import utils
from game import models


def test_conjugate_points():
    assert utils.conjugate_points(0) == "punktów"
    assert utils.conjugate_points(1) == "punkt"
    assert utils.conjugate_points(2) == "punkty"
    assert utils.conjugate_points(5) == "punktów"
    with pytest.raises(ValueError):
        utils.conjugate_points(-1)
    with pytest.raises(ValueError):
        utils.conjugate_points(11)


@pytest.mark.django_db
def test_create_ten_questions():
    assert models.Question.objects.count() == 0
    utils.create_ten_questions()
    assert models.Question.objects.count() == 10


@pytest.mark.django_db
def test_get_or_create_quiz_gets_current_quiz_if_exists(current_quiz):
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 1
    quiz = utils.get_or_create_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_current_quiz_from_existing_questions(questions):
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_or_create_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_quiz_for_specific_week_from_existing_questions(questions):
    year = 2000
    week = 1
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_or_create_quiz(year=year, week=week)
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_current_quiz_even_if_there_are_no_questions():
    year, week, day = now().isocalendar()
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_or_create_quiz()
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


@pytest.mark.django_db
def test_get_or_create_quiz_creates_quiz_for_specific_week_even_if_there_are_no_questions():
    year = 2000
    week = 1
    assert models.Quiz.objects.count() == 0
    quiz = utils.get_or_create_quiz(year=year, week=week)
    assert models.Quiz.objects.count() == 1
    assert quiz.year == year
    assert quiz.week == week


def test_conjugate_days():
    assert utils.conjugate_days(1) == "dzień"
    assert utils.conjugate_days(2) == "dni"
    with pytest.raises(ValueError):
        utils.conjugate_days(0)
    with pytest.raises(ValueError):
        utils.conjugate_days(-1)
    with pytest.raises(ValueError):
        utils.conjugate_days(8)


def test_conjuagte_hours():
    assert utils.conjugate_hours(1) == "godzina"
    assert utils.conjugate_hours(2) == "godziny"
    assert utils.conjugate_hours(5) == "godzin"
    with pytest.raises(ValueError):
        utils.conjugate_hours(0)
    with pytest.raises(ValueError):
        utils.conjugate_hours(-1)
    with pytest.raises(ValueError):
        utils.conjugate_hours(25)


def test_conjugate_minutes():
    assert utils.conjugate_minutes(1) == "minuta"
    assert utils.conjugate_minutes(2) == "minuty"
    assert utils.conjugate_minutes(5) == "minut"
    with pytest.raises(ValueError):
        utils.conjugate_minutes(0)
    with pytest.raises(ValueError):
        utils.conjugate_minutes(-1)
    with pytest.raises(ValueError):
        utils.conjugate_minutes(61)


def test_get_remaining_time_in_week():
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 27, 0, 0)) == "1 dzień, 23 godziny i 59 minut"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 27, 12, 15)) == "1 dzień, 11 godzin i 44 minuty"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 28, 22, 55)) == "1 godzina i 4 minuty"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 28, 23, 45)) == "14 minut"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 26, 23, 45)) == "2 dni, 14 minut"


# @pytest.mark.django_db
# def test_get_match_context(current_quiz, user):
#     assert utils.get_match_context(current_quiz, user, nest=False) == {"exists": False, "quiz": current_quiz}
