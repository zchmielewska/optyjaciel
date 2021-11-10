import pandas as pd
import numpy as np


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

