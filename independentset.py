"""
This module contains routines concerning the maximum independent set problem.
"""
from bitset import iterate, subsets, size

def check_independent(graph, subset):
    for v in iterate(subset):
        for w in iterate(subset):
            if v > w and graph(v) & w:
                return False
    return True

def bruteforce(graph):
    max_size = 0
    max_is = None
    for subset in subsets(graph.vertices):
        if size(subset) > max_size and check_independent(graph, subset):
            max_is = subset
            max_size = size(subset)
    return max_is
