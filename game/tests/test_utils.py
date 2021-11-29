import datetime
import pytest

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


def test_get_remaining_time_in_week():
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 27, 0, 0)) == "1 dzień, 23 godziny i 59 minut"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 27, 12, 15)) == "1 dzień, 11 godzin i 44 minuty"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 28, 22, 55)) == "1 godzina i 4 minuty"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 28, 23, 45)) == "14 minut"
    assert utils.get_remaining_time_in_week(datetime.datetime(2021, 11, 26, 23, 45)) == "2 dni, 14 minut"


def test_conjugate_points():
    assert utils.conjugate_points(0) == "punktów"
    assert utils.conjugate_points(1) == "punkt"
    assert utils.conjugate_points(2) == "punkty"
    assert utils.conjugate_points(5) == "punktów"
    with pytest.raises(ValueError):
        utils.conjugate_points(-1)
    with pytest.raises(ValueError):
        utils.conjugate_points(11)
