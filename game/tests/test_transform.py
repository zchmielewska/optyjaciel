import numpy as np
import pandas as pd
import pytest

from game.utils import transform


@pytest.mark.django_db
def test_get_answers(quiz_with_questions):
    assert transform.get_answers(quiz_with_questions) == 1


def test_answers_to_scores_matrix():
    a1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    a2 = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]
    a3 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    s1 = np.array([10])
    s2 = np.array([[10, 3], [3, 10]])
    s3 = np.array([[10, 3, 0], [3, 10, 2], [0, 2, 10]])
    assert transform.answers_to_scores_matrix(pd.DataFrame([a1])) == s1
    assert (transform.answers_to_scores_matrix(pd.DataFrame([a1, a2])) == s2).all()
    assert (transform.answers_to_scores_matrix(pd.DataFrame([a1, a2, a3])) == s3).all()

    a4 = [1, 2, 3]
    with pytest.raises(ValueError):
        transform.answers_to_scores_matrix(pd.DataFrame([a4]))

    with pytest.raises(ValueError):
        transform.answers_to_scores_matrix(pd.DataFrame([]))
