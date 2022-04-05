from django.core.management.base import BaseCommand
from game.utils.db_control import fill_with_questions
from game import models


class Command(BaseCommand):
    help = "Create random quiz for the given year and week"

    def add_arguments(self, parser):
        parser.add_argument("year", type=int)
        parser.add_argument("week", type=int)

    def handle(self, *args, **options):
        year = options["year"]
        week = options["week"]
        quiz = models.Quiz.objects.create(year=year, week=week)
        fill_with_questions(quiz)
