from django.core.management.base import BaseCommand
from game.utils.utils import send_emails_after_game


class Command(BaseCommand):
    help = "Send emails after game"

    def handle(self, *args, **options):
        send_emails_after_game()
