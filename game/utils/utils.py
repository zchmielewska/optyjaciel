import arrow
import datetime
import django.utils.timezone
import django.db
import game.models
import random
from django.contrib.auth.models import User

def get_current_quiz():
    """
    Retrieves quiz for the current week.
    If the quiz doesn't exist, it creates one and populates with random questions.

    :return: quiz object
    """
    year, week, day = django.utils.timezone.now().isocalendar()
    quizes = game.models.Quiz.objects.filter(year=year, week=week)
    no_quizes = quizes.count()

    if no_quizes == 1:
        return quizes.first()
    elif no_quizes == 0:
        return create_random_quiz(year, week)
    else:
        raise ValueError("There should be only one quiz per week.")


def get_remaining_time_in_week():
    """
    Creates a string that informs about time to the end of week.
    Time is presented as number of days, hours in minutes.
    String is in Polish and respects conjugation rules.
    Example: 5 dni, 6 godzin i 27 minut

    :return: string
    """
    now = arrow.get(django.utils.timezone.now())
    week_end = now.ceil('week')
    diff = week_end - now

    days_count = diff.days
    hours_count = diff.seconds//3600
    minutes_count = (diff.seconds//60) % 60

    days_text = conjugate_days(days_count)
    hours_text = conjugate_hours(hours_count)
    minutes_text = conjugate_minutes(minutes_count)

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


def get_match_context(quiz, user, nest=True):
    """
    Prepares context for the match template.
    The nest flag is used so that the function can be used for two views:
        - view for single match (for the current game),
        - view for multiple matches (for the historical games).

    :param quiz: quiz object
    :param user: user object
    :param nest: boolean, should the context be included in an additional dictionary?
    :return: context for the match template
    """
    match = game.models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()

    if not match.matched_user:
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


def get_text_answer(quiz_question, user):
    """
    Retrieves an answer of the user for the given quiz question.
    An answer is returned as a text (rather than number)

    :param quiz_question: quiz_question object
    :param user: user object
    :return: string
    """
    answer_object = game.models.Answer.objects.get(user=user, quiz_question=quiz_question)
    answer = answer_object.answer

    if answer == 1:
        result = quiz_question.question.option1
    elif answer == 2:
        result = quiz_question.question.option2
    elif answer == 3:
        result = quiz_question.question.option3
    else:
        result = quiz_question.question.option4

    return result


def create_random_quiz(year, week):
    """
    Creates a quiz and populates it with random questions.
    The function tries to use questions that weren't yet used in other quizes.
    If that's not possible, it populates the quiz with questions already used in other quizes.

    :param year: year of the quiz
    :param week: week of the quiz
    :return: quiz object
    """
    with django.db.transaction.atomic():
        quiz = game.models.Quiz.objects.create(year=year, week=week)

        # Some questions might not have been yet used
        unused = game.models.Question.objects.filter(quizquestion__isnull=True).distinct()
        used = game.models.Question.objects.filter(quizquestion__isnull=False).distinct()

        n = len(unused)

        # Quiz should have as many unused questions as possible
        if n >= 10:
            questions = random.sample(list(unused), 10)
        elif n >= 1:
            questions = list(unused) + random.sample(list(used), 10-n)
        else:
            questions = random.sample(list(used), 10)

        # Add questions to the quiz
        for i in range(10):
            game.models.QuizQuestion.objects.create(
                quiz=quiz,
                question=questions[i],
                question_index=i+1,
            )
    return quiz


def calculate_score(quiz, user1, user2):
    """
    Calculates the number of questions for which two users answered in the same way.

    :param quiz: quiz object
    :param user1: first user object
    :param user2: second user object
    :return: integer
    """
    quiz_questions = quiz.quizquestion_set.order_by("question_index")
    score = 0
    for quiz_question in quiz_questions:
        answer1 = game.models.Answer.objects.get(user=user1, quiz_question=quiz_question)
        answer2 = game.models.Answer.objects.get(user=user2, quiz_question=quiz_question)
        if answer1.answer == answer2.answer:
            score += 1

    return score


def conjugate_days(days_count):
    """
    Conjugates number of days in Polish.

    :param days_count: number of days
    :return: string
    """
    days_text = None
    if days_count == 1:
        days_text = f"{days_count} dzień"
    else:
        days_text = f"{days_count} dni"
    return days_text


def conjugate_hours(hours_count):
    """
    Conjugates number of hours in Polish.

    :param hours_count: number of hours
    :return: string
    """
    hours_text = None
    if hours_count == 1:
        hours_text = f"{hours_count} godzina"
    elif 2 <= hours_count <= 4 or 22 <= hours_count <= 24:
        hours_text = f"{hours_count} godziny"
    elif 5 <= hours_count <= 21:
        hours_text = f"{hours_count} godzin"
    else:
        raise ValueError("Number of hours shoud be between 1 and 24.")
    return hours_text


def conjugate_minutes(minutes_count):
    """
    Conjugates number of minutes in Polish.

    :param minutes_count: number of minutes
    :return: string
    """
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
            55 <= minutes_count <= 59:
        minutes_text = f"{minutes_count} minut"
    else:
        raise ValueError("Number of minutes should be between 1 and 59.")
    return minutes_text


def conjugate_points(number):

    """
    Conjugates the word "points" in Polish for different number of points.

    :param number: number of points
    :return: conjugated word
    """
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


def get_users_previous_quizes(user):
    # Current game is ignored
    current_quiz = get_current_quiz()

    # User might have participated only in few historical quizes
    answers = game.models.Answer.objects.filter(user=user)
    quiz_questions = [answer.quiz_question for answer in answers]
    quizes = set()
    for quiz_question in quiz_questions:
        if quiz_question.quiz != current_quiz:
            quizes.add(quiz_question.quiz)

    return quizes


def get_matches_context(user):
    quizes = get_users_previous_quizes(user)
    matches_context = []
    for quiz in quizes:
        match = game.utils.utils.get_match_context(quiz, user, nest=False)
        matches_context.append(match)
    return matches_context


def get_matches_queryset(user):
    quizes = get_users_previous_quizes(user)
    matched_users_ids = set()
    for quiz in quizes:
        match = game.models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()
        matched_users_ids.add(match.matched_user_id)
    matches = User.objects.filter(pk__in=matched_users_ids)
    return matches
