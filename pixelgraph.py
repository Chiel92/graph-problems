"""
This module contains the PixelGraph class.
"""

from graph import Graph
from bitset import bit, bits

class PixelGraph(Graph):

    """
    A PixelGraph is a planar graph for which each vertex can be represented as an adjacent
    group of cells (called planes) in a grid and each edge equates adjacency of planes.
    To avoid computational conversion between the two representations, we store them
    both synchronically.
    """

    def __init__(self, grid):
        """The grid is a 2d array of numbers."""
        self.grid = grid

        for row in grid:
            if len(row) != self.grid_width:
                raise ValueError('Input grid is not a valid matrix.')
            for col in grid[row]:
                if grid[row][col] < 0:
                    raise ValueError('Input grid has negative numbers.')


        # TODO: make sure planes with the same number are adjacent

        # Detect and create vertices
        vertex_numbers = set(grid[row][col] for row in grid for col in grid[row])
        vertices = bits(*vertex_numbers)

        # Detect and create neighborhoods
        neighborhoods = {}
        for row in grid:
            for col in grid[row]:
                current_pixel_vertex = bit(grid[row][col])

                try:
                    right_pixel_vertex = bit(grid[row][col+1])
                except IndexError:
                    pass
                else:
                    neighborhoods[current_pixel_vertex] |= right_pixel_vertex

                try:
                    lower_pixel_vertex = bit(grid[row+1][col])
                except IndexError:
                    pass
                else:
                    neighborhoods[current_pixel_vertex] |= lower_pixel_vertex

        Graph.__init__(self, vertices, neighborhoods)

    @property
    def grid_height(self):
        return len(self.grid)

    @property
    def grid_width(self):
        return len(self.grid[0])


def generate_random(grid_height, grid_width, nr_planes):
    grid = []
