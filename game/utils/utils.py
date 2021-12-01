import arrow
from django.utils.timezone import now


def conjugate_days(days_count):
    """
    Conjugates number of days (in a week) in Polish language.

    :param days_count: integer, number of days
    :return: string
    """
    if days_count == 1:
        days_text = "dzień"
    elif 2 <= days_count <= 7:
        days_text = "dni"
    else:
        raise ValueError("Count of days must be between 1 and 7.")
    return days_text


def conjugate_hours(hours_count):
    """
    Conjugates number of hours (in a day) in Polish language.

    :param hours_count: integer, number of hours
    :return: string
    """
    if hours_count == 1:
        hours_text = "godzina"
    elif 2 <= hours_count <= 4 or 22 <= hours_count <= 24:
        hours_text = "godziny"
    elif 5 <= hours_count <= 21:
        hours_text = "godzin"
    else:
        raise ValueError("Number of hours must be between 1 and 24.")
    return hours_text


def conjugate_minutes(minutes_count):
    """
    Conjugates number of minutes (in an hour) in Polish language.

    :param minutes_count: integer, number of minutes
    :return: string
    """
    if minutes_count == 1:
        minutes_text = "minuta"
    elif 2 <= minutes_count <= 4 or \
            22 <= minutes_count <= 24 or \
            32 <= minutes_count <= 34 or \
            42 <= minutes_count <= 44 or \
            52 <= minutes_count <= 54:
        minutes_text = "minuty"
    elif 5 <= minutes_count <= 21 or \
            25 <= minutes_count <= 31 or \
            35 <= minutes_count <= 41 or \
            45 <= minutes_count <= 51 or \
            55 <= minutes_count <= 60:
        minutes_text = "minut"
    else:
        raise ValueError("Number of minutes must be between 1 and 60.")
    return minutes_text


def get_remaining_time_in_week(moment=None):
    """
    Creates a string that informs about the time until the end of the week in Polish language.
    Time is presented as number of days, hours and minutes.
    If no argument is passed, the function uses the current moment.
    Output example: 5 dni, 6 godzin i 27 minut

    :return: string
    """
    if not moment:
        moment = now()

    arrow_moment = arrow.get(moment)
    week_end = arrow_moment.ceil('week')
    diff = week_end - arrow_moment

    days_count = diff.days
    hours_count = diff.seconds//3600
    minutes_count = (diff.seconds//60) % 60

    days_text = f"{days_count} {conjugate_days(days_count)}" if days_count > 0 else None
    hours_text = f"{hours_count} {conjugate_hours(hours_count)}" if hours_count > 0 else None
    minutes_text = f"{minutes_count} {conjugate_minutes(minutes_count)}" if minutes_count > 0 else None

    result = minutes_text
    result = hours_text + " i " + result if hours_text else result
    result = days_text + ", " + result if days_text else result
    return result


def conjugate_points(points_count):
    """
    Conjugates number of points (in a range 0 to 10) in Polish language.

    :param points_count: number of points
    :return: conjugated word
    """
    if points_count == 0:
        result = "punktów"
    elif points_count == 1:
        result = "punkt"
    elif 2 <= points_count <= 4:
        result = "punkty"
    elif 5 <= points_count <= 10:
        result = "punktów"
    else:
        raise ValueError("Number of points must be between 0 and 10.")
    return result
