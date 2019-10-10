from heuristics.constructive import *
from operator import itemgetter


def choose_solution_features(solution):
    features = []

    return features


def choose_penalty_features(solution, features):
    util = []

    i = 0
    for i in range(0, features[i].__len__()):
        if features[i] in solution:
            util[i] = features[i]['cost'] / (1 + features[i]['penalty'])
            features[i]['util'] = util[i]

    penalized_features = sorted(features, key=itemgetter('util'), reverse=True)  # sort the list by the desc util values
    n = 0  # return the N features which will be penalized
    return penalized_features[0:n]


def local_search(solution, h):

    if h:
        solution = solution['value'] + h

    return solution


def guided_local_search(dataset, k, m, depot):
    """
    This function do...
    """
    k = 0
    current_solution = constructive_heuristic(dataset)
    best_solution = current_solution
    features = choose_solution_features(current_solution)
    penalties = []
    # penalty = {'id': '','penalty': '', 'cost': ''}

    while k <= 10:  # k is the number of iterations without improvement

        penalties = choose_penalty_features(features)

        i = 0
        for i in range(0, penalties[i].__len__()):
            if features[i]['id'] in penalties:
                features[i]['penalty'] = features[i]['penalty'] + 1

        neighbor_solution = local_search(best_solution, h)  # h is true if you wanna apply penalties in the solution

        if neighbor_solution < best_solution:
            best_solution = neighbor_solution
            k = 0

        best_solution = local_search(best_solution, h)  # h is false to catch the real optimal local in the solution without penalties
        k = k + 1

    return best_solution
