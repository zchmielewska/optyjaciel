import arrow
import datetime
import django.utils.timezone
import django.db
import game.models
import random


def get_current_quiz():
    """
    Retrieves quiz for the current week.
    If the quiz doesn't exist, it creates a random one.

    :return: quiz object
    """
    year, week, day = django.utils.timezone.now().isocalendar()
    quizes = game.models.Quiz.objects.filter(year=year, week=week)

    if len(quizes) == 1:
        return quizes[0]
    elif len(quizes) == 0:
        return create_random_quiz(year, week)
    else:
        raise ValueError("There should be only one quiz per week.")


def create_random_quiz(year, week):
    with django.db.transaction.atomic():
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

    days_count = diff.days
    hours_count = diff.seconds//3600
    minutes_count = (diff.seconds//60) % 60

    days_text = None
    if days_count == 1:
        days_text = f"{days_count} dzień"
    else:
        days_text = f"{days_count} dni"

    hours_text = None
    if hours_count == 1:
        hours_text = f"{hours_count} godzina"
    elif 2 <= hours_count <= 4 or 22 <= hours_count <= 24:
        hours_text = f"{hours_count} godziny"
    elif 5 <= hours_count <= 21:
        hours_text = f"{hours_count} godzin"

    minutes_text = None
    if minutes_count == 1:
        minutes_text = f"{minutes_count} minuta"
    elif 2 <= minutes_count <= 4 or \
            22 <= minutes_count <= 24 or \
            32 <= minutes_count <= 34 or \
            42 <= minutes_count <= 44 or \
            52 <= minutes_count <= 54:
        minutes_text = f"{minutes_count} minuty"
    elif 5 <= minutes_count <= 21 or \
            25 <= minutes_count <= 31 or \
            35 <= minutes_count <= 41 or \
            45 <= minutes_count <= 51 or \
            55 <= minutes_count:
        minutes_text = f"{minutes_count} minut"

    # Example: 5 dni, 6 godzin i 27 minut
    result = ""
    if days_text:
        result += days_text
        if hours_text or minutes_text:
            result += ", "

    if hours_text:
        result += hours_text
        if minutes_text:
            result += " i " + minutes_text

    return result


def calculate_score(quiz, user1, user2):
    quiz_items = quiz.quizitem_set.order_by("question_set_index")
    score = 0
    for quiz_item in quiz_items:
        answer1 = game.models.Answer.objects.get(user=user1, quiz_item=quiz_item)
        answer2 = game.models.Answer.objects.get(user=user2, quiz_item=quiz_item)
        if answer1.answer == answer2.answer:
            score += 1

    return score


def conjugate_points(number):
    if number == 0:
        result = "punktów"
    elif number == 1:
        result = "punkt"
    elif 2 <= number <= 4:
        result = "punkty"
    elif 5 <= number <= 10:
        result = "punktów"
    else:
        result = "punkty"
    return result


def get_match_context(quiz, user, nest=True):
    """
    :param quiz: quiz object
    :param user: user object
    :param nest: boolean, should the context be included in an additional dictionary?

    Return context for the match template.
    The nest flag is used so that the function can be used for both: single match and multiple matches.
    Single match is used for the current game's results and multiple matches are used for historical matches.

    :return: context for the match template
    """
    match = game.models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()

    if not match:
        inner_data = {
            "exists": False,
            "quiz": quiz
        }
        context = {"match": inner_data} if nest else inner_data
    else:
        matched_user = match.matched_user
        score = game.utils.utils.calculate_score(quiz, user, matched_user)
        points = game.utils.utils.conjugate_points(score)
        inner_data = {
            "exists": True,
            "quiz": quiz,
            "user": user,
            "matched_user": matched_user,
            "score": score,
            "points": points,
        }
        context = {"match": inner_data} if nest else inner_data
    return context
