from bitset import iterate, size, subtract, contains, first
from components import components
from utils import Infinity


def get_neighborhood(N, subset):
    result = 0
    for v in iterate(subset):
        result |= N[v]
    return result


def get_neighborhood_2(N, subset):
    result = get_neighborhood(N, subset)
    for v in iterate(result):
        result |= N[v]
    return result


def increment_un(G, X, UN_X, v):
    """Compute UN of X|v, based on the UN of X"""
    U = set()
    for S in UN_X:
        U.add(subtract(S, v))
        U.add(subtract(S, v) | (G.neighborhoods[v] & (G.vertices - (X | v))))
    return U


def check_decomposition(G, decomposition):
    un = {0}
    lboolw = 1
    left = 0
    right = G.vertices

    for v in decomposition:
        un = increment_un(G, left | v, v, un)
        lboolw = max(lboolw, len(un))
        left = left | v
        right = subtract(right, v)

    return lboolw


def incremental_un_heuristic(G):
    lboolw_components = []
    decomposition_components = []

    for component in components(G):
        best_lboolw = Infinity
        best_decomposition = None
        for i, start in enumerate([first(component)]):
        #for i, start in enumerate(iterate(component)):
            print('{}th starting vertex'.format(i))
            right = subtract(component, start)
            left = start
            un_left = increment_un(G, 0, {0}, start)
            booldim_left = 1

            decomposition = [start]
            lboolw = len(un_left)

            for _ in range(size(component) - 1):
                best_vertex, best_un, _ = greedy_step(G, left, right, un_left,
                                                      booldim_left, {}, Infinity)
                booldim_left = len(best_un)
                lboolw = max(lboolw, booldim_left)
                un_left = best_un

                decomposition.append(best_vertex)
                right = subtract(right, best_vertex)
                left = left | best_vertex

            if lboolw < best_lboolw:
                best_lboolw = lboolw
                best_decomposition = decomposition
        lboolw_components.append(best_lboolw)
        decomposition_components.append(best_decomposition)

    total_lboolw = max(lboolw_components)
    total_decomposition = [v for part in decomposition_components for v in part]

    return total_lboolw, total_decomposition


def greedy_step(G, left, right, un_left, booldim_left, un_table, bound):
    best_vertex = None
    best_booldim = Infinity
    best_un = None

    if size(right) == 1:
        return right, {0}, 1

    assert size(right) > 1

    candidates = get_neighborhood_2(G.neighborhoods, left) & right

    # Trivial cases are slow
    for v in iterate(candidates):
        if trivial_case(G.neighborhoods, left, right, v):
            new_un = increment_un(G, left, un_left, v)
            new_booldim = len(new_un)
            return v, new_un, new_booldim

    for v in iterate(candidates):
        if left | v not in un_table:
            un_table[left | v] = increment_un(G, left, un_left, v)
        new_un = un_table[left | v]
        new_booldim = len(new_un)

        # Apply pruning
        if new_booldim >= bound:
            # print('pruning')
            continue

        if new_booldim < best_booldim:
            best_vertex = v
            best_booldim = new_booldim
            best_un = new_un

    # If nothing found
    if best_vertex == None:
        best_un = increment_un(G, left, un_left, v)
        best_booldim = len(best_un)
        best_vertex = v

    assert best_vertex != None
    return best_vertex, best_un, best_booldim


def trivial_case(N, left, right, v):
    # No neighbors
    if contains(left, N[v]):
        return True

    # Twins
    for u in iterate(left):
        if N[v] & right == subtract(N[u], v) & right:
            return True

    return False

