from pixelgraph import *
from plot import plot
from independentset import bruteforce, heuristic
from bitset import tostring

grid = matrix_to_dict([
    [0, 0, 5, 5, 5],
    [0, 0, 0, 1, 5],
    [2, 2, 4, 1, 5],
    [3, 2, 3, 1, 5],
    [3, 3, 3, 3, 6],
])

grid = random_walk(10, 10, 10)

graph = PixelGraph(grid)
print(graph)
plot(graph)
print(tostring(bruteforce(graph)))
print(tostring(heuristic(graph)))
