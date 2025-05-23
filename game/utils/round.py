import datetime
import pandas as pd
import random
from datetime import datetime
from django.db.models import Min

from game.models import Match, Question, Quiz, QuizQuestion
from game.utils.db_control import calculate_score
from game.utils.transform import get_answers, answers_to_scores_matrix, match_matrix_to_match_table
from game.utils import solver


def create_matches_from_quiz(quiz):
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
    print(f"Starting new round for {current_date}...")

    quiz = Quiz.objects.create(date=current_date)
    questions = choose_questions()

    # Add questions to the quiz
    for i in range(10):
        count = QuizQuestion.objects.filter(quiz=quiz, question_index=i + 1).count()
        if count == 0:
            QuizQuestion.objects.create(
                quiz=quiz,
                question=questions[i],
                question_index=i + 1,
            )
    return quiz


def choose_questions():
    print("Choosing questions...")
    quiz_size = 10

    # 1. Retrieve all distinct categories
    all_categories = list(Question.objects
                          .order_by()
                          .values_list('category', flat=True)
                          .distinct())
    print("Categories:", all_categories)

    # 2. Randomly choose quiz_size categories (repeating if needed)
    if len(all_categories) >= quiz_size:
        chosen_categories = random.sample(all_categories, quiz_size)
    else:
        chosen_categories = all_categories.copy()
        while len(chosen_categories) < quiz_size:
            chosen_categories.append(random.choice(all_categories))
    print("Chosen categories:", chosen_categories)

    selected_questions = set()

    # 3. For each chosen category, pick one least-used, unique question
    for category in chosen_categories:
        print("category =", category)
        category_qs = Question.objects.filter(category=category)

        # Exclude selected questions
        category_qs = category_qs.exclude(id__in=[q.id for q in selected_questions])

        # If there are no questions available, continue
        if not category_qs.exists():
            continue

        # Find the minimum times_selected in this category
        min_times = category_qs.aggregate(min_ts=Min('times_selected'))['min_ts'] or 0

        # Filter to questions with that minimum counter
        least_used = category_qs.filter(times_selected=min_times)

        # Randomly select one
        pick = random.choice(list(least_used))
        print("pick =", pick)
        selected_questions.add(pick)

        # If you have 10 questions, then stop
        if len(selected_questions) == quiz_size:
            break

    # 4. Increment times_selected for each selected question
    for question in selected_questions:
        question.times_selected += 1
        question.save(update_fields=['times_selected'])

    return list(selected_questions)


def delete_current_round():
    print("Deleting current round...")
    current_date = datetime.now().strftime("%Y%m%d")
    Quiz.objects.filter(date=current_date).delete()
