import arrow
import datetime
import django.utils.timezone
import game.models
import random


def get_current_quiz():
    year, week, day = django.utils.timezone.now().isocalendar()
    quizes = game.models.Quiz.objects.filter(year=year, week=week)

    if len(quizes) == 1:
        return quizes[0]
    elif len(quizes) == 0:
        return create_random_quiz(year, week)
    else:
        raise ValueError("There should be only one quiz per week.")


def create_random_quiz(year, week):
    question_sets = random.sample(list(game.models.QuestionSet.objects.all()), 10)
    quiz = game.models.Quiz.objects.create(
        year=year,
        week=week,
        question_set0=question_sets[0],
        question_set1=question_sets[1],
        question_set2=question_sets[2],
        question_set3=question_sets[3],
        question_set4=question_sets[4],
        question_set5=question_sets[5],
        question_set6=question_sets[6],
        question_set7=question_sets[7],
        question_set8=question_sets[8],
        question_set9=question_sets[9],
    )
    return quiz


def get_remaining_time_in_week():
    now = arrow.get(django.utils.timezone.now())
    week_end = now.ceil('week')
    diff = week_end - now
    days = diff.days
    hours = str(datetime.timedelta(seconds=diff.seconds))
    return f"{days} dni i {hours} godzin"
