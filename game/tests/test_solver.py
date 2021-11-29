import numpy as np

from game.utils import solver


def test_match():
    s1 = np.array([10])
    m1 = np.array([0])
    assert solver.match(s1) == m1

    s2 = np.array([[10, 3], [3, 10]])
    m2 = np.array([[0, 1], [1, 0]])
    assert (solver.match(s2) == m2).all()

    s3 = np.array([
        [10, 7, 8, 2],
        [7, 10, 3, 4],
        [8, 3, 10, 6],
        [2, 4, 6, 10]
    ])
    m3 = np.array([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    assert (solver.match(s3) == m3).all()
