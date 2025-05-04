import datetime
import logging
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand

from game.models import Match, Quiz
from game.utils.db_control import calculate_score, fill_with_questions
from game.utils.transform import get_answers, answers_to_scores_matrix, match_matrix_to_match_table
from game.utils import solver


logging.basicConfig(
    filename="end_round.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def end_last_round():
    logging.info("Starting the quiz matching process.")

    quiz = Quiz.objects.order_by('-id').first()
    logging.info(f"Processing matches for Quiz ID {quiz.id}, Date: {quiz.date}")

    answers, users_id = get_answers(quiz)
    if answers is None:
        logging.warning("No answers retrieved. Skipping this round.")
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
    logging.info(f"Started new quiz round with ID {new_quiz.id} on {current_date}")


class Command(BaseCommand):
    help = "Calculates and saves matches for the latest quiz and creates a new quiz."

    def handle(self, *args, **kwargs):
        end_last_round()
        start_new_round()

