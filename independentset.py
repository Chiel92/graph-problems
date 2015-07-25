"""
This module contains routines concerning the maximum independent set problem.
"""
from bitset import iterate, subsets, size, subtract
from utils import Infinity, argmax

def is_independent(graph, subset):
    for v in iterate(subset):
        for w in iterate(subset):
            if v > w and graph(v) & w:
                return False
    return True

def bruteforce(graph):
    max_size = 0
    max_is = None
    for subset in subsets(graph.vertices):
        if size(subset) > max_size and is_independent(graph, subset):
            max_is = subset
            max_size = size(subset)
    return max_is

def heuristic(graph):
    subset = 0
    while is_independent(graph, subset):
        # Find valid vertex with the least new neighbors
        existing_neighbors = graph(subset)
        min_new_neighbors = Infinity
        new_vertex = None
        for v in iterate(subtract(graph.vertices, subset)):
            if not graph(v) & subset:
                new_neighbors = subtract(graph(v), existing_neighbors)
                if size(new_neighbors) < min_new_neighbors:
                    min_new_neighbors = size(new_neighbors)
                    new_vertex = v

        if new_vertex == None:
            return subset
        else:
            subset |= new_vertex

def from_decomposition(graph, decomposition):
    # Make hash function depend on neighborhood
    solutions = {graph(0): 0}
    right = graph.vertices

    def add(collection, solution):
        key = graph(solution) & right
        if key not in collection or size(collection[key]) < size(solution):
            collection[key] = solution

    for v in decomposition:
        new_solutions = {}
        right -= v
        for solution in solutions.values():
            add(new_solutions, solution)
            if is_independent(graph, solution | v):
                add(new_solutions, solution | v)
        solutions = new_solutions

    result = argmax(solutions.values(), key=size)
    assert is_independent(graph, result)
    return result

