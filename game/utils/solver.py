import numpy as np
import pulp


def match(scores):
    """
    Matches users into pairs based on the scores matrix.
    Scores matrix contains the number of points for each pair of users.
    Match matrix contains zero-one values. The value of one means a match between two users.
    Each row of the match matrix can have value of one maximally once.
    The aim of optimization is maximization of points in the whole group.

    :param scores: matrix with scores
    :return: matrix with matches
    """
    n = len(scores)
    result = np.zeros((n, n))
    possible_matches = [pm for pm in pulp.permutation(range(n), 2)]
    x = pulp.LpVariable.dicts("if_match", possible_matches, lowBound=0, upBound=1, cat=pulp.LpInteger)
    model = pulp.LpProblem("matching_model", pulp.LpMaximize)

    # Objective function
    goal = sum([scores[pm[0]][pm[1]] * x[pm] for pm in possible_matches])
    model += goal

    # Constraints
    # [1/4]
    for i in range(n):
        model += sum(x[(i, j)] for j in range(n) if i != j) <= 1, f"One_match_per_row_{i}"

    # [2/4]
    for j in range(n):
        model += sum(x[(i, j)] for i in range(n) if i != j) <= 1, f"One_match_per_column_{j}"

    # [3/4]
    for i in range(n):
        for j in range(n):
            if i != j:
                model += x[(i, j)] - x[(j, i)] == 0, f"Symmetrical_pair_{i}_{j}"

    # [4/4]
    if n % 2 == 0:
        model += sum(x[(i, j)] for i in range(n) for j in range(n) if i != j) == n, "Maximal_number_of_matches"
    else:
        model += sum(x[(i, j)] for i in range(n) for j in range(n) if i != j) == n-1, "Maximal_number_of_matches"

    # Solver
    solution_found = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if solution_found == -1:
        result = None
    else:
        for key, value in x.items():
            result[key[0], key[1]] = x[key].value()

    return result
