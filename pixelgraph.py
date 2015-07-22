"""
This module contains the PixelGraph class.
"""

class PixelGraph:

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

        # Create vertices
        for row in grid:
            for col in grid[row]:

    @property
    def grid_height(self):
        return len(self.grid)

    @property
    def grid_width(self):
        return len(self.grid[0])


def generate_random(grid_height, grid_width, nr_planes):
    grid = []
