from django.core.management.base import BaseCommand

from game.tasks import send_something_to_me


class Command(BaseCommand):
    help = "Send random to admin."

    def handle(self, *args, **options):
        send_something_to_me()
