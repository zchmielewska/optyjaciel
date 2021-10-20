import numpy as np
import pulp


# scores1 = [[ 0, 10,  2,  7],
#            [10,  0,  8,  1],
#            [ 2,  8,  0,  4],
#            [ 7,  1,  4,  0]]
#
# # Maximal number of matches (4th contraint)
# scores2 = [[ 0, 10,  0,  0],
#            [10,  0,  0,  0],
#            [ 0,  0,  0,  0],
#            [ 0,  0,  0,  0]]
#
# # Odd number of participants
# scores3 = [[ 0, 10,  2,  4,  3],
#            [10,  0,  8, 10,  3],
#            [ 2,  8,  0,  2,  3],
#            [ 4, 10,  2,  0,  3],
#            [ 3,  3,  3,  3,  3]]


def derive_match_matrix(scores):
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
    solution_found = model.solve()
    if solution_found == -1:
        result = null
    else:
        for key, value in x.items():
            result[key[0], key[1]] = x[key].value()

    return result


# Tests:
# print(derive_match_matrix(scores1))
# print(derive_match_matrix(scores2))
# print(derive_match_matrix(scores3))

