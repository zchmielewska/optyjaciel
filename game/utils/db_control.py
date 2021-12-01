import django.db
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
        {'question': 'Jaką porę roku lubisz najbardziej?', 'option1': 'lato', 'option2': 'jesień',
         'option3': 'zima', 'option4': 'wiosna'},
        {'question': 'Ulubiony kolor?', 'option1': 'czerwony', 'option2': 'zielony',
         'option3': 'niebieski', 'option4': 'żółty'},
        {'question': 'Najsilniejszy superbohater?', 'option1': 'Superman', 'option2': 'Wonder Woman',
         'option3': 'Batman', 'option4': 'Spider-man'},
        {'question': 'Najsmaczniejsza potrawa?', 'option1': 'pizza', 'option2': 'sałatka',
         'option3': 'sushi', 'option4': 'zupa pomidorowa'},
        {'question': 'Najbardziej wciągający serial?', 'option1': 'przyjaciele', 'option2': 'teoria wielkiego podrywu',
         'option3': 'gra o tron', 'option4': 'głowa rodziny'},
        {'question': 'Jakie masz lub chciał(a)byś mieć zwierzę?', 'option1': 'kot', 'option2': 'pies',
         'option3': 'rybki', 'option4': 'papuga'},
        {'question': 'Jaki sport uprawiasz albo oglądasz?', 'option1': 'piłka nożna', 'option2': 'tenis',
         'option3': 'pływanie', 'option4': 'jazda na nartach'},
        {'question': 'Ulubiony smak lodów?', 'option1': 'czekoladowe', 'option2': 'waniliowe',
         'option3': 'truskawkowe', 'option4': 'pistacjowe'},
        {'question': 'Gdzie najchętniej spędzasz czas?', 'option1': 'plaża', 'option2': 'las',
         'option3': 'miasto', 'option4': 'góry'},
        {'question': 'Ulubiona gra planszowa?', 'option1': 'szachy', 'option2': 'monopol',
         'option3': 'scrabble', 'option4': 'jenga'}
    ]

    questions = []
    for datum in data:
        question = models.Question.objects.create(**datum)
        questions.append(question)

    return questions


def fill_quiz_with_questions(quiz):
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
        fill_quiz_with_questions(quiz)

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

    if answer == 1:
        result = quiz_question.question.option1
    elif answer == 2:
        result = quiz_question.question.option2
    elif answer == 3:
        result = quiz_question.question.option3
    else:
        result = quiz_question.question.option4

    return result


def get_users_previous_quizes(user):
    """
    Returns a list of quiz objects in which the user has participated.
    The list is ordered in reverse-chronological order (newest first).

    :param user: user object
    :return: list of quiz objects
    """
    # Current game gets ignored
    year, week, day = now().isocalendar()
    current_quiz = get_quiz(year=year, week=week)

    # User might have participated only in few historical quizes
    answers = models.Answer.objects.filter(user=user)
    quiz_questions = [answer.quiz_question for answer in answers]
    quizes = []
    for quiz_question in quiz_questions:
        if quiz_question.quiz != current_quiz and quiz_question.quiz not in quizes:
            quizes.append(quiz_question.quiz)

    quizes.sort(key=lambda x: (x.year, x.week), reverse=True)

    return quizes


def get_match_context(quiz, user, nest=True):
    """
    Prepares context for the match template.

    The nest flag is used so that the function can be used for two views:
        - view for single match (for the current game),
        - view for multiple matches (for the previous games).

    The context contains all variables used within the template:
        - exists - does the match exist,
        - quiz - for which quiz is the match,
        - user - logged-in user object,
        - matched_user - match user object,
        - score - number of points,
        - points - conjugated word points.

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


def get_matches_context(user):
    quizes = get_users_previous_quizes(user)
    matches_context = []
    for quiz in quizes:
        match = get_match_context(quiz, user, nest=False)
        matches_context.append(match)
    return matches_context


def get_matches_queryset(user):
    quizes = get_users_previous_quizes(user)
    matched_users_ids = set()
    for quiz in quizes:
        match = models.Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()
        matched_users_ids.add(match.matched_user_id)
    matches = User.objects.filter(pk__in=matched_users_ids)
    return matches
