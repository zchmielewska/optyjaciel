import numpy as np


def answers_to_scores_matrix(df):
    n = len(df.index)
    scores = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            scores[i, j] = sum(df.iloc[i] == df.iloc[j])

    return scores
