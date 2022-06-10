import random
from django.contrib.auth.models import User
from django.utils.timezone import now

from game import models
from game.utils import utils


def create_ten_questions():
    """
    Adds ten questions to the DB.
    Quizes and questions should be managed manually by staff.
    However, if the manual work hasn't been done, the app should not crash.
    For the app to work independently (without human interaction), it needs at least 10 questions in the DB.

    :return: list with 10 question objects
    """
    data = [
        {'question': 'Pora roku', 'option1': 'lato', 'option2': 'zima'},
        {'question': 'Czas', 'option1': 'przeszłość', 'option2': 'przyszłość'},
        {'question': 'Mój charakter', 'option1': 'ekstrawertyk', 'option2': 'introwertyk'},
        {'question': 'Wakacje', 'option1': 'w górach', 'option2': 'nad morzem'},
        {'question': 'Do pływania', 'option1': 'basen', 'option2': 'jezioro'},
        {'question': 'Zwierzę domowe', 'option1': 'kot', 'option2': 'pies'},
        {'question': 'Czas wolny', 'option1': 'impreza', 'option2': 'wieczór w domu'},
        {'question': 'Przedmiot szkolny', 'option1': 'matematyka', 'option2': 'język polski'},
        {'question': 'Superbohater', 'option1': 'batman', 'option2': 'superman'},
        {'question': 'Dom magii', 'option1': 'Gryfindor', 'option2': 'Slytherin'}
    ]

    questions = []
    for datum in data:
        question = models.Question.objects.create(**datum)
        questions.append(question)

    return questions


def fill_with_questions(quiz):
    """
    Fills quiz with questions (if they are not present).
    Tries to use as many questions that weren't used in other quizes as possible.
    No impact if the quiz already has 10 questions.

    :param quiz: quiz object to which questions will be added
    :return: quiz object with filled questions
    """
    n_lacking_questions = 10 - quiz.questions.count()

    # There must be at least 10 questions in db to create a quiz
    n_questions = models.Question.objects.count()
    if n_questions < 10:
        create_ten_questions()

    # Some questions might not have been yet used
    unused = models.Question.objects.filter(quizquestion__isnull=True).distinct()
    used = models.Question.objects.filter(quizquestion__isnull=False).distinct()
    n_unused = len(unused)

    # Quiz should have as many unused questions as possible
    if n_unused >= n_lacking_questions:
        questions = random.sample(list(unused), n_lacking_questions)
    elif n_unused >= 1:
        questions = list(unused) + random.sample(list(used), n_lacking_questions - n_unused)
    else:
        questions = random.sample(list(used), n_lacking_questions)

    # Add questions to the quiz
    for i in range(10):
        count = models.QuizQuestion.objects.filter(quiz=quiz, question_index=i+1).count()
        if count == 0:
            models.QuizQuestion.objects.create(
                quiz=quiz,
                question=questions[i],
                question_index=i+1,
            )
    return quiz


def get_quiz(year, week):
    """
    Retrieves quiz for the given week. If the quiz doesn't exist yet, it gets created.
    Ensures that the quiz has 10 questions.

    :param year: integer
    :param week: integer
    :return: quiz object
    """
    quizes = models.Quiz.objects.filter(year=year, week=week)
    no_quizes = quizes.count()

    if no_quizes > 1:
        raise ValueError("There should be only one quiz per week.")
    elif no_quizes == 1:
        quiz = quizes.first()
    elif no_quizes == 0:
        quiz = models.Quiz.objects.create(year=year, week=week)

    # Quiz must have 10 questions but staff could manually add less
    if not quiz.questions.count() == 10:
        fill_with_questions(quiz)

    return quiz


def get_current_quiz():
    """
    Retrieves quiz for the current week.

    :return: quiz object
    """
    year, week, day = now().isocalendar()
    quiz = get_quiz(year=year, week=week)
    return quiz


def calculate_score(quiz, user1, user2):
    """
    Calculates the number of questions for which two users answered in the same way.

    :param quiz: quiz object
    :param user1: first user object
    :param user2: second user object
    :return: integer in range 0-10
    """
    quiz_questions = quiz.quizquestion_set.order_by("question_index")
    score = 0
    for quiz_question in quiz_questions:
        answer1 = models.Answer.objects.get(user=user1, quiz_question=quiz_question)
        answer2 = models.Answer.objects.get(user=user2, quiz_question=quiz_question)
        if answer1.answer == answer2.answer:
            score += 1

    return score


def get_text_answer(quiz_question, user):
    """
    Retrieves user's answer for the quiz question.
    An answer is returned as a text (rather than number)

    :param quiz_question: quiz question object
    :param user: user object
    :return: string
    """
    answer_object = models.Answer.objects.get(user=user, quiz_question=quiz_question)
    answer = answer_object.answer
    return quiz_question.question.option1 if answer == 1 else quiz_question.question.option2


def remove_current_quiz(quizes):
    year, week, day = now().isocalendar()
    current_quiz = get_quiz(year=year, week=week)
    if current_quiz in quizes:
        quizes.remove(current_quiz)
    return quizes


def list_quizes(user, previous=True):
    """
    Returns a list of quiz objects in which the user has participated.
    The list is ordered in reverse-chronological order (newest first).

    :param previous: exclude the current quiz
    :param user: user object
    :return: list of quiz objects
    """
    # User doesn't have to participate in all quizes
    answers = models.Answer.objects.filter(user=user)
    quiz_questions = [answer.quiz_question for answer in answers]
    all_quizes = [quiz_question.quiz for quiz_question in quiz_questions]
    quizes = list(set(all_quizes))  # only unique quizes

    # If previous is set, current game gets ignored
    if previous:
        quizes = remove_current_quiz(quizes)

    quizes.sort(key=lambda x: (x.year, x.week), reverse=True)
    return quizes


def get_match_context(quiz, user, nest=True):
    """
    Prepares context for the match template.

    The nest flag is used so that the function can be used for two views:
        - view for single match (for the current game),
        - view for multiple matches (for the previous games) - used within a loop.

    The context contains all variables used within the template:
        - exists - does the match exist,
        - quiz - for which quiz is the match,
        - user - logged-in user,
        - matched_user - user who is a match,
        - score - number of points,
        - points - conjugated word "points".

    If there is no match (due to uneven number of participants), only 'exists' and 'quiz' are included in the context.

    :param quiz: quiz object
    :param user: user object
    :param nest: boolean, should the context be included in an additional dictionary?
    :return: context for the match template
    """
    match = models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()

    if not match.matched_user:
        inner_data = {
            "exists": False,
            "quiz": quiz
        }
        context = {"match": inner_data} if nest else inner_data
    else:
        matched_user = match.matched_user
        score = calculate_score(quiz, user, matched_user)
        points = utils.conjugate_points(score)
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


def get_matches_queryset(user, quizes=None, previous=True):
    """
    Returns a queryset of matches from quizes.
    Includes only active users.

    :param user: user object
    :param quizes: subset of quizes (all, if not specified)
    :param previous: exclude the current quiz
    :return: queryset of user objects
    """
    if not quizes:
        quizes = list_quizes(user)

    if previous:
        quizes = remove_current_quiz(quizes)

    matched_users_ids = set()
    for quiz in quizes:
        match = models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()
        matched_users_ids.add(match.matched_user_id)
    matches = User.objects.filter(pk__in=matched_users_ids).filter(is_active=True)
    return matches


def user_participated_in_quiz(user, quiz):
    """
    Checks if user has participated in a quiz.

    :param user: user object
    :param quiz: quiz object
    :return: boolean
    """
    quizes = list_quizes(user, previous=False)
    return quiz in quizes


def user_is_match_with(user1, user2):
    """
    Checks if two users are matches in any of the quizes.

    :param user1: user object
    :param user2: user object
    :return: boolean
    """
    matches = get_matches_queryset(user1, previous=False)
    result = user2 in matches
    return result


def list_participants(quiz_id):
    matches = models.Match.objects.filter(quiz_id=quiz_id)
    users_id = set()
    for match in matches:
        users_id.add(match.user_id)
    return list(users_id)
