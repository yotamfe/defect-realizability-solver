import numpy as np
import itertools
import random
from abc import ABC, abstractmethod

class Lattice(ABC):
    def __init__(self, x_length, y_length, z_length):
        self._x_length = x_length
        self._y_length = y_length
        self._z_length = z_length

        # A cell is identified by the (x,y,z) coordinates of its left lower vertex.
        # An edge is identified by the (x,y,z) coordinates of the vertex where it starts
        # (with the convention that the lattice is directed away from the origin),
        # and the direction in the lattice it goes to.

        self._defects_edgeset = set()

    @abstractmethod
    def cell_orientations(self):
        pass

    def iter_cells(self):
        return itertools.product(range(self._x_length), range(self._y_length), range(self._z_length))

    def iter_edges(self):
        return itertools.chain(
            itertools.product(range(self._x_length), range(self._y_length - 1), range(self._z_length - 1), [0]),
            itertools.product(range(self._x_length - 1), range(self._y_length), range(self._z_length - 1), [1]),
            itertools.product(range(self._x_length - 1), range(self._y_length - 1), range(self._z_length), [2]),
        )

    def is_defect(self, edge):
        return edge in self._defects_edgeset

    @abstractmethod
    def edge_adjacent_orientation_blocks(self, edge):
        pass

    def generate_defect_assignment(self, random_defect_probability):
        for edge in self.iter_edges():
            if random.random() < random_defect_probability:
                self._defects_edgeset.add(edge)

        self._make_even_num_defects_per_cell()

    def _iter_internal_cells(self):
        return itertools.product(range(self._x_length - 1), range(self._y_length - 1), range(self._z_length - 1))

    def _has_even_num_of_defects(self, cell):
        x, y, z = cell
        assert x < self._x_length
        assert y < self._y_length
        assert z < self._z_length
        cell_edges = set([(x, y, z, 0), (x + 1, y, z, 0),
                          (x, y, z, 1), (x, y + 1, z, 1),
                          (x, y, z, 2), (x, y, z + 1, 2)])
        cell_defects = cell_edges & self._defects_edgeset
        return len(cell_defects) % 2 == 0

    def _toggle_defect(self, edge):
        if edge in self._defects_edgeset:
            self._defects_edgeset.remove(edge)
        else:
            self._defects_edgeset.add(edge)

    def _make_even_num_defects_per_cell(self):
        for cell in self._iter_internal_cells():
            if self._has_even_num_of_defects(cell):
                continue
            x, y, z = cell
            self._toggle_defect((x + 1, y, z, 0))

    @abstractmethod
    def save_to_file(self, path):
        pass
