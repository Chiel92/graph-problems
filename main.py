from pixelgraph import *
from plot import plot
from independentset import bruteforce, heuristic, from_decomposition
from bitset import tostring, iterate, size
from lboolw_heuristic import incremental_un_heuristic

from random import randint

#grid = matrix_to_dict([
    #[0, 0, 5, 5, 5],
    #[0, 0, 0, 1, 5],
    #[2, 2, 4, 1, 5],
    #[3, 2, 3, 1, 5],
    #[3, 3, 3, 3, 6],
#])

while 1:
    width = randint(5, 35)
    height = 40 - width
    max_field_size = randint(5, 25)
    grid = random_walk(width, height, max_field_size)

    graph = PixelGraph(grid)
    width, decomposition = incremental_un_heuristic(graph)
    heuristic_solution = heuristic(graph)
    exact_solution = from_decomposition(graph, decomposition)
    if size(heuristic_solution) < size(exact_solution) - 3:
        break

print(graph)
print(tostring(heuristic_solution))
print(tostring(exact_solution))
#Possible engines: dot, neato, fdp, sfdp, twopi, circo
plot(graph, 'neato')

#print(tostring(from_decomposition(graph, iterate(graph.vertices))))
#print(tostring(bruteforce(graph)))
