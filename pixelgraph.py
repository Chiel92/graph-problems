"""
This module contains the PixelGraph class.
"""

from graph import Graph
from bitset import bit, bits
from random import choice


class PixelGraph(Graph):

    """
    A PixelGraph is a planar graph for which each vertex can be represented as an adjacent
    group of cells (called fields) in a grid and each edge equates adjacency of fields.
    To avoid computational conversion between the two representations, we store them
    both synchronically.
    """

    def __init__(self, grid_dict):
        """The grid is a 2d array of numbers."""
        self.grid_dict = grid_dict
        self.grid_matrix = dict_to_matrix(grid_dict)

        for row in self.grid_matrix:
            if len(row) != self.grid_width:
                raise ValueError('Input grid is not a valid matrix.')
            for val in row:
                if val < 0:
                    raise ValueError('Input grid has negative numbers.')

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
        return len(self.grid_matrix)

    @property
    def grid_width(self):
        return len(self.grid_matrix[0])

    def __str__(self):
        return '\n'.join(' '.join(['{:4}'.format(val) for val in row])
                         for row in self.grid_matrix)

#
# UTILS
#


def neighbor_cells(cell_domain, current_cell):
    row, col = current_cell
    for cell in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if cell in cell_domain:
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


def dict_to_matrix(grid_dict):
    matrix = []
    row = 0
    while (row, 0) in grid_dict:
        matrix.append([])
        col = 0
        while (row, col) in grid_dict:
            matrix[row].append(grid_dict[row, col])
            col += 1
        row += 1
    return matrix


def matrix_to_dict(matrix):
    return {(y, x): number for y, row in enumerate(matrix)
            for x, number in enumerate(row)}

#
# GENERATORS
#


def random_walk(grid_height, grid_width, max_field_size):
    unassigned = {(y, x) for x in range(grid_width) for y in range(grid_height)}
    grid_dict = {}

    number = 0
    while unassigned:
        cell = unassigned.pop()
        grid_dict[cell] = number
        for _ in range(max_field_size - 1):
            unassigned_neighbors = list(neighbor_cells(unassigned, cell))
            try:
                next_cell = choice(unassigned_neighbors)
                unassigned.remove(next_cell)
            except IndexError:
                break
            else:
                cell = next_cell
                grid_dict[cell] = number
        number += 1

    return grid_dict

