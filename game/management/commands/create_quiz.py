from django.core.management.base import BaseCommand
from game.utils.utils import create_random_quiz


class Command(BaseCommand):
    help = "Create random quiz for the given year and week"

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('week', type=int)

    def handle(self, *args, **options):
        create_random_quiz(options['year'], options['week'])
