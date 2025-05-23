"""IMPORTANT: Connected to Heroku Scheduler"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from game.models import Match, Quiz
from game.utils.db_control import get_participants
from game.utils import round


def send_emails_after_round(quiz):
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
        round.create_matches_from_quiz(last_quiz)
        round.start_new_round()
        send_emails_after_round(last_quiz)
