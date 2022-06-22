import arrow
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now

from game.utils import db_control
from game import models


DOMAIN = settings.DEFAULT_DOMAIN


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


def string_is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def send_emails_after_game():
    """
    Send e-mails to all participants after the game is over.

    E-mails are sent on Monday.
    Only active users with active matches should receive e-mail.
    """
    # Emails should be sent after game
    today_is_monday = (datetime.datetime.today().weekday() == 0)
    if not today_is_monday:
        return None

    # Information is sent on the last week's quiz
    current_quiz_id = db_control.get_current_quiz().id
    quiz_id = current_quiz_id - 1
    quiz = models.Quiz.objects.get(id=quiz_id)

    # List of participants ids
    participants_id = db_control.list_participants(quiz_id)

    # Send e-mails
    for participant_id in participants_id:
        participant = User.objects.get(id=participant_id)
        if participant.is_active:
            match = models.Match.objects.filter(quiz=quiz, user=participant).order_by("-matched_at").first()
            matched_user = User.objects.get(id=match.matched_user_id)
            if matched_user.is_active:
                score = db_control.calculate_score(quiz, participant, matched_user)
                ctx = {
                    "quiz": quiz,
                    "participant": participant,
                    "matched_user": matched_user,
                    "score": score,
                    "domain": DOMAIN,
                }
                pass
                subject = f"optyjaciel | nowy optyjaciel w rundzie {quiz.year}_{quiz.week}"
                html_message = render_to_string("email/end-game.html", ctx)
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, plain_message, from_email, [participant.email, ], html_message=html_message,
                          fail_silently=False)
    return None

