from django.contrib.auth.models import User
from game import models


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
    if answer == 1:
        return quiz_question.question.option1
    elif answer == 2:
        return quiz_question.question.option2
    elif answer == 3:
        return quiz_question.question.option3
    elif answer == 4:
        return quiz_question.question.option4
    else:
        return "Unknown answer"


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
        context = {
            "exists": True,
            "quiz": quiz,
            "user": user,
            "matched_user": match.matched_user,
            "score": match.score,
        }
    return context


def get_matches_queryset(user):
    """
    Returns a queryset of matches from quizes. Includes only active users.

    :param user: user object 
    :return: queryset of user objects
    """
    quizes = list_quizes(user)
    matched_users_ids = set()

    for quiz in quizes:
        match = models.Match.objects.get(quiz=quiz, user=user)
        matched_users_ids.add(match.matched_user_id)

    matches = User.objects.filter(pk__in=matched_users_ids).filter(is_active=True)
    return matches


def participated_in_quiz(user, quiz):
    """
    Checks if user has participated in a quiz.

    :param user: user object
    :param quiz: quiz object
    :return: boolean
    """
    quizes = list_quizes(user)
    return quiz in quizes


def is_match_with(user1, user2):
    """Checks if two users are matches in any of the quizes."""
    matches = get_matches_queryset(user1)
    result = user2 in matches
    return result


def get_participants(quiz):
    """List of users who played in quiz"""
    matches = models.Match.objects.filter(quiz=quiz)
    users_id = set()
    for match in matches:
        users_id.add(match.user_id)
    return list(users_id)
