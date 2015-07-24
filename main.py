from pixelgraph import PixelGraph
from plot import plot
from independentset import bruteforce, heuristic
from bitset import tostring

grid = [
    [0, 0, 5, 5, 5],
    [0, 0, 0, 1, 5],
    [2, 2, 4, 1, 5],
    [3, 2, 3, 1, 5],
    [3, 3, 3, 3, 6],
]


graph = PixelGraph(grid)
plot(graph)
print(tostring(bruteforce(graph)))
print(tostring(heuristic(graph)))
