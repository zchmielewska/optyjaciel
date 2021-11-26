import pytest
from django.utils.timezone import now
from game.utils import utils


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
def test_get_or_create_quiz_gets_quiz():
    pass


@pytest.mark.django_db
def test_get_or_create_quiz_creates_quiz_when_doesnt_exists(questions):
    year, week, day = now().isocalendar()
    quiz = utils.get_or_create_quiz(year=year, week=week)
    assert quiz.id == 1
    assert quiz.year == year
    assert quiz.week == week

