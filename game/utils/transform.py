import pandas as pd
import numpy as np

from game import models
from game.utils import solver


def get_answers(quiz):
    """
    Prepares the table (data frame) with answers for the given quiz and list of users ids.
    The table has 10 column, one for each question.
    Each row of the table are answers of one user.

    The list contains users ids in the same order as the table.
    For example, the answers in the first row were given by the user with id located in the first element of the list.

    :param quiz:
    :return: table with answers, list with users ids
    """
    answers_list = []
    for i in range(10):
        question_index = i + 1
        quiz_question = quiz.quizquestion_set.get(question_index=question_index)
        quiz_question_answers = quiz_question.answer_set.order_by("user_id")
        if question_index == 1:
            df = pd.DataFrame(list(quiz_question_answers.values("user_id", "answer")))
        else:
            df = pd.DataFrame(list(quiz_question_answers.values("answer")))
        df = df.rename(columns={"answer": "answer" + str(question_index)})
        answers_list.append(df)

    df = pd.concat(answers_list, axis=1)
    answers = df[["answer" + str(i + 1) for i in range(10)]]
    users_id = list(df["user_id"])
    return answers, users_id


def answers_to_scores_matrix(answers):
    """
    Calculates the scores matrix based on the answers table.
    Scores matrix has the dimension of the number of users.
    Values in the matrix are the number of questions to which users answered in the same way.

    :param answers: pandas data frame with answers
    :return: numpy 2d array with scores
    """
    if not len(answers.columns) == 10:
        raise ValueError("Answers table must have 10 columns.")

    if not len(answers.index) > 0:
        raise ValueError("Answers table must have at least 1 row.")

    n = len(answers.index)
    scores = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            scores[i, j] = sum(answers.iloc[i] == answers.iloc[j])

    return scores


def match_matrix_to_match_table(match_matrix, users_id):
    """
    Transforms match matrix into match table.
    Match table contains two columns:
     - user - id of the user,
     - matched_user - id of the user's match.

    :param match_matrix: matrix with boolean values representing matches
    :param users_id: list of users' ids
    :return: table with matches
    """
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
    """
    Gets answers of all users and recalculates matches.
    Saves new matches.

    :param quiz: quiz for which new matches are recalculated
    :return: None
    """
    answers, users_id = get_answers(quiz)
    scores = answers_to_scores_matrix(answers)
    match_matrix = solver.match(scores)
    match_table = match_matrix_to_match_table(match_matrix, users_id)

    for index, row in match_table.iterrows():
        matched_user_id = row["matched_user"] if not pd.isnull(row["matched_user"]) else None
        models.Match.objects.create(quiz=quiz, user_id=row["user"], matched_user_id=matched_user_id)
