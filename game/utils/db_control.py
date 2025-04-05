import random
from django.contrib.auth.models import User
from django.utils import timezone
from game import models


def get_current_quiz():
    quiz = models.Quiz.objects.order_by('-id').first()
    return quiz


def get_quiz(date):
    quiz = models.Quiz.objects.get(date=date)
    return quiz


def fill_with_questions(quiz):
    questions = models.Question.objects.all()
    questions = random.sample(list(questions), 10)

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


def calculate_score(quiz, user1, user2):
    quiz_questions = quiz.quizquestion_set.order_by("question_index")
    score = 0
    for quiz_question in quiz_questions:
        answer1 = models.Answer.objects.get(user=user1, quiz_question=quiz_question)
        answer2 = models.Answer.objects.get(user=user2, quiz_question=quiz_question)
        if answer1.answer == answer2.answer:
            score += 1

    return score


def get_text_answer(quiz_question, user):
    answer_object = models.Answer.objects.get(user=user, quiz_question=quiz_question)
    answer = answer_object.answer
    return quiz_question.question.option1 if answer == 1 else quiz_question.question.option2


def remove_current_quiz(quizes):
    today = timezone.now()
    formatted_date = today.strftime('%Y%m%d')
    current_quiz = get_quiz(date=formatted_date)
    if current_quiz in quizes:
        quizes.remove(current_quiz)
    return quizes


def list_quizes(user):
    matches = models.Match.objects.filter(user=user)
    quizes = [match.quiz for match in matches]
    quizes.sort(key=lambda x: (x.date), reverse=True)
    return quizes


def get_match_context(quiz, user):
    match = models.Match.objects.get(quiz=quiz, user=user)
    if match.matched_user is None:   # Odd number of players
        context = {
            "exists": False,
            "quiz": quiz
        }
    else:
        matched_user = match.matched_user
        score = calculate_score(quiz, user, matched_user)
        context = {
            "exists": True,
            "quiz": quiz,
            "user": user,
            "matched_user": matched_user,
            "score": score,
        }
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

    # if previous:
    #     quizes = remove_current_quiz(quizes)

    matched_users_ids = set()
    for quiz in quizes:
        match = models.Match.objects.get(quiz=quiz, user=user)
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