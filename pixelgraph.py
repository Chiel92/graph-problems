"""
This module contains the PixelGraph class.
"""

from graph import Graph
from bitset import bit, bits


def neighbor_cells(grid_dict, current_cell):
    row, col = current_cell
    for cell in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if cell in grid_dict:
            yield cell


def explore(grid_dict):
    todo = [cell for cell in grid_dict]
    fields = []

    while todo:
        front = [todo.pop()]
        field = front[:]

        while front:
            current_cell = front.pop()
            current_color = grid_dict[current_cell]
            for neighbor_cell in neighbor_cells(grid_dict, current_cell):
                if neighbor_cell in todo and grid_dict[neighbor_cell] == current_color:
                    front.append(neighbor_cell)
                    field.append(neighbor_cell)
                    todo.remove(neighbor_cell)
        fields.append(field)
    print(fields)


class PixelGraph(Graph):

    """
    A PixelGraph is a planar graph for which each vertex can be represented as an adjacent
    group of cells (called fields) in a grid and each edge equates adjacency of fields.
    To avoid computational conversion between the two representations, we store them
    both synchronically.
    """

    def __init__(self, grid):
        """The grid is a 2d array of numbers."""
        self.grid = grid

        for row in grid:
            if len(row) != self.grid_width:
                raise ValueError('Input grid is not a valid matrix.')
            for val in row:
                if val < 0:
                    raise ValueError('Input grid has negative numbers.')

        # Mapping from cells to numbers
        grid_dict = {(y, x): number for y, row in enumerate(grid)
                     for x, number in enumerate(row)}

        # Detect fields by BFS
        todo = [cell for cell in grid_dict]
        fields = {}  # Mapping from field number to group of cells

        while todo:
            front = [todo.pop()]
            field = front[:]
            current_number = grid_dict[field[0]]
            if current_number in fields:
                raise ValueError(
                    'Not all cells with the same number are in the same field'
                )

            while front:
                current_cell = front.pop()
                for neighbor_cell in neighbor_cells(grid_dict, current_cell):
                    if neighbor_cell in todo and grid_dict[neighbor_cell] == current_number:
                        front.append(neighbor_cell)
                        field.append(neighbor_cell)
                        todo.remove(neighbor_cell)
            fields[current_number] = field
        self.fields = fields

        # Detect and create vertices
        vertex_numbers = fields.keys()
        vertices = bits(*vertex_numbers)

        # Detect and create neighborhoods
        neighborhoods = {}
        for number, cells in fields.items():
            neighbors = 0
            for cell in cells:
                for neighbor_cell in neighbor_cells(grid_dict, cell):
                    neighbors |= bit(grid_dict[neighbor_cell])
            neighborhoods[bit(number)] = neighbors

        Graph.__init__(self, vertices, neighborhoods)

    @property
    def grid_height(self):
        return len(self.grid)

    @property
    def grid_width(self):
        return len(self.grid[0])


def generate_random(grid_height, grid_width, nr_fields):
    grid = []

