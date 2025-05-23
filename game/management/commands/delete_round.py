from django.core.management.base import BaseCommand

from game.utils import round


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        round.delete_current_round()
