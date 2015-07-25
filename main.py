from pixelgraph import *
from plot import plot
from independentset import bruteforce, heuristic, from_decomposition
from bitset import tostring, iterate
from lboolw_heuristic import incremental_un_heuristic

#grid = matrix_to_dict([
    #[0, 0, 5, 5, 5],
    #[0, 0, 0, 1, 5],
    #[2, 2, 4, 1, 5],
    #[3, 2, 3, 1, 5],
    #[3, 3, 3, 3, 6],
#])

grid = random_walk(20, 20, 20)

graph = PixelGraph(grid)
print(graph)
#Possible engines: dot, neato, fdp, sfdp, twopi, circo
plot(graph, 'neato')

width, decomposition = incremental_un_heuristic(graph)


print(tostring(heuristic(graph)))
print(tostring(from_decomposition(graph, decomposition)))
#print(tostring(from_decomposition(graph, iterate(graph.vertices))))
#print(tostring(bruteforce(graph)))
