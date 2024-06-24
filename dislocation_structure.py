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

        self._dislocations_edgeset = set()

    @abstractmethod
    def cell_alignments(self):
        pass

    def iter_cells(self):
        return itertools.product(range(self._x_length), range(self._y_length), range(self._z_length))

    def iter_edges(self):
        return itertools.chain(
            itertools.product(range(self._x_length), range(self._y_length - 1), range(self._z_length - 1), [0]),
            itertools.product(range(self._x_length - 1), range(self._y_length), range(self._z_length - 1), [1]),
            itertools.product(range(self._x_length - 1), range(self._y_length - 1), range(self._z_length), [2]),
        )

    def is_dislocation(self, edge):
        return edge in self._dislocations_edgeset

    @abstractmethod
    def edge_adjacent_alignments(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), a),
                    ((x, y + 1, z), a),
                    ((x, y, z + 1), a),
                    ((x, y + 1, z + 1), a)]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), a),
                    ((x + 1, y, z), a),
                    ((x, y, z + 1), a),
                    ((x + 1, y, z + 1), a)]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return      [((x, y, z), a),
                     ((x + 1, y, z), a),
                     ((x, y + 1, z), a),
                     ((x + 1, y + 1, z), a)]

    def generate_dislocation_assignment(self, random_dislocation_probability):
        for edge in self.iter_edges():
            if random.random() < random_dislocation_probability:
                self._dislocations_edgeset.add(edge)

        self._make_even_num_dislocations_per_cell()

    def _iter_internal_cells(self):
        return itertools.product(range(self._x_length - 1), range(self._y_length - 1), range(self._z_length - 1))

    def _has_even_num_of_dislocations(self, cell):
        x, y, z = cell
        assert x < self._x_length
        assert y < self._y_length
        assert z < self._z_length
        cell_edges = set([(x, y, z, 0), (x + 1, y, z, 0),
                          (x, y, z, 1), (x, y + 1, z, 1),
                          (x, y, z, 2), (x, y, z + 1, 2)])
        cell_dislocations = cell_edges & self._dislocations_edgeset
        return len(cell_dislocations) % 2 == 0

    def _toggle_dislocation(self, edge):
        if edge in self._dislocations_edgeset:
            self._dislocations_edgeset.remove(edge)
        else:
            self._dislocations_edgeset.add(edge)

    def _make_even_num_dislocations_per_cell(self):
        for cell in self._iter_internal_cells():
            if self._has_even_num_of_dislocations(cell):
                continue
            x, y, z = cell
            self._toggle_dislocation((x + 1, y, z, 0))

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Odd" if self.is_dislocation(edge) else "Even"
                x, y, z, a = edge
                f.write(f"{x} {y} {z} {constraint}\n")
