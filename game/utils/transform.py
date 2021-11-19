import pandas as pd
import numpy as np
from .solver import match
from game.models import *


def get_answers(quiz):
    answers_list = []
    for i in range(10):
        question_set_index = i + 1
        quiz_item = quiz.quizitem_set.get(question_set_index=question_set_index)
        quiz_item_answers = quiz_item.answer_set.all().order_by("user_id")
        if question_set_index == 1:
            df = pd.DataFrame(list(quiz_item_answers.values("user_id", "answer")))
        else:
            df = pd.DataFrame(list(quiz_item_answers.values("answer")))
        df = df.rename(columns={"answer": "answer" + str(question_set_index)})
        answers_list.append(df)

    df = pd.concat(answers_list, axis=1)
    answers = df[["answer" + str(i + 1) for i in range(10)]]
    users_id = list(df["user_id"])
    return answers, users_id


def answers_to_scores_matrix(df):
    n = len(df.index)
    scores = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            scores[i, j] = sum(df.iloc[i] == df.iloc[j])

    return scores


def match_matrix_to_match_table(match_matrix, users_id):
    data = []
    n = len(users_id)
    for i in range(n):
        for j in range(n):
            if match_matrix[i, j] == 1:
                data.append([users_id[i], users_id[j]])
                break
            else:
                if j == n-1:
                    data.append([users_id[i], None])

    match_table = pd.DataFrame(data, columns=["user", "matched_user"])
    return match_table


def recalculate_and_save_matches(quiz):
    # Get answers of all users and recalculate matches
    answers, users_id = get_answers(quiz)
    scores = answers_to_scores_matrix(answers)
    match_matrix = match(scores)
    match_table = match_matrix_to_match_table(match_matrix, users_id)

    # Save new matches
    for index, row in match_table.iterrows():
        matched_user_id = row["matched_user"] if not pd.isnull(row["matched_user"]) else None
        Match.objects.create(quiz=quiz, user_id=row["user"], matched_user_id=matched_user_id)
