import arrow
import datetime
import django.utils.timezone
from django.db import transaction

import game.models
import random


def get_current_quiz():
    year, week, day = django.utils.timezone.now().isocalendar()
    quizes = game.models.Quiz.objects.filter(year=year, week=week)

    if len(quizes) == 1:
        return quizes[0]
    elif len(quizes) == 0:
        return create_random_quiz(year, week)  # TODO adjust to new model structure
    else:
        raise ValueError("There should be only one quiz per week.")


def create_random_quiz(year, week):
    with transaction.atomic():
        quiz = game.models.Quiz.objects.create(year=year, week=week)

        # Some question sets might not have been yet used
        unused = game.models.QuestionSet.objects.filter(quizitem__isnull=True).distinct()
        used = game.models.QuestionSet.objects.filter(quizitem__isnull=False).distinct()

        n = len(unused)

        # Quiz should have as many unused question sets as possible
        if n >= 10:
            question_sets = random.sample(list(unused), 10)
        elif n >= 1:
            question_sets = list(unused) + random.sample(list(used), 10-n)
        else:
            question_sets = random.sample(list(used), 10)

        # Add quiz items to the quiz
        for i in range(10):
            game.models.QuizItem.objects.create(
                quiz=quiz,
                question_set_index=i+1,
                question_set=question_sets[i],
            )
    return quiz


def get_remaining_time_in_week():
    now = arrow.get(django.utils.timezone.now())
    week_end = now.ceil('week')
    diff = week_end - now
    days = diff.days
    hours = str(datetime.timedelta(seconds=diff.seconds))
    return f"{days} dni i {hours} godzin"
