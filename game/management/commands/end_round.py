import datetime
import pandas as pd
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from game.models import Match, Quiz
from game.utils.db_control import calculate_score, fill_with_questions, get_participants
from game.utils.transform import get_answers, answers_to_scores_matrix, match_matrix_to_match_table
from game.utils import solver


def end_last_round():
    quiz = Quiz.objects.order_by('-id').first()
    answers, users_id = get_answers(quiz)

    if answers is None:
        return None

    scores = answers_to_scores_matrix(answers)
    match_matrix = solver.match(scores)
    match_table = match_matrix_to_match_table(match_matrix, users_id)

    for index, row in match_table.iterrows():
        matched_user_id = row["matched_user"]
        user_id = row["user"]

        # Odd number of players
        if (matched_user_id == user_id) or pd.isnull(row["matched_user"]):
            matched_user_id = None

        # Create a Match
        if not Match.objects.filter(quiz=quiz, user_id=user_id, matched_user_id=matched_user_id).exists():
            if matched_user_id is not None:
                score = calculate_score(quiz, user_id, matched_user_id)
            else:
                score = 0
            Match.objects.create(quiz=quiz, user_id=user_id, matched_user_id=matched_user_id, score=score)


def start_new_round():
    current_date = datetime.now().strftime("%Y%m%d")
    new_quiz = Quiz.objects.create(date=current_date)
    fill_with_questions(new_quiz)


def send_emails_after_game(quiz):
    # List of participants ids
    participants_id = get_participants(quiz)

    # Send e-mails
    for participant_id in participants_id:
        participant = User.objects.get(id=participant_id)
        match = Match.objects.get(quiz=quiz, user=participant)

        if match.matched_user is None:
            send_mail(
                subject=f"optyjaciel | brak optyjaciela w rundzie {quiz.date}",
                message="Niestety, w tej rundzie było nieparzyście osób i nie zostałeś sparowany/a.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[participant.email, ],
                fail_silently=True
            )
        else:
            ctx = {
                "quiz": quiz,
                "participant": participant,
                "matched_user": match.matched_user,
                "score": match.score,
                "domain": settings.DEFAULT_DOMAIN,
            }
            subject = f"optyjaciel | nowy optyjaciel w rundzie {quiz.date}"
            html_message = render_to_string("email/end-game.html", ctx)
            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[participant.email, ],
                html_message=html_message,
                fail_silently=True
            )
    return None


class Command(BaseCommand):
    help = "Calculates and saves matches for the latest quiz and creates a new quiz."

    def handle(self, *args, **kwargs):
        last_quiz = Quiz.objects.order_by('-id').first()
        end_last_round()
        start_new_round()
        send_emails_after_game(last_quiz)
