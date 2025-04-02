import pandas as pd
from django.core.management.base import BaseCommand

from game.models import Match, Quiz
from game.utils.transform import get_answers, answers_to_scores_matrix, match_matrix_to_match_table
from game.utils import solver


class Command(BaseCommand):
    help = "Recalculates and saves matches for the latest quiz."

    def handle(self, *args, **kwargs):
        quiz = Quiz.objects.order_by('-id').first()
        if not quiz:
            self.stderr.write(self.style.ERROR('No quizzes found.'))
            return

        self.stdout.write(self.style.NOTICE(f'Recalculating matches for latest quiz ID {quiz.id}...'))
        answers, users_id = get_answers(quiz)
        scores = answers_to_scores_matrix(answers)
        match_matrix = solver.match(scores)
        match_table = match_matrix_to_match_table(match_matrix, users_id)

        for index, row in match_table.iterrows():
            matched_user_id = row["matched_user"] if not pd.isnull(row["matched_user"]) else None
            Match.objects.create(quiz=quiz, user_id=row["user"], matched_user_id=matched_user_id)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(match_table)} matches.'))
