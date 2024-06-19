import numpy as np
import itertools
import random

import pysat
from pysat.formula import CNF, And, Or, XOr, Neg, Atom, PYSAT_TRUE
import pysat.solvers
import pysat.card

class Lattice:
    def __init__(self, x_length, y_length, z_length):
        self._x_length = x_length
        self._y_length = y_length
        self._z_length = z_length
        self._alignments = [0, 1, 2]

        # A cell is identified by the (x,y,z) coordinates of its left lower vertex.
        # An edge is identified by the (x,y,z) coordinates of the vertex where it starts
        # (with the convention that the lattice is directed away from the origin),
        # and the direction in the lattice it goes to.

        self._dislocations_edgeset = set()

    def cell_alignments(self):
        return self._alignments

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
        # TODO: ensure assingment has another property

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Odd" if self.is_dislocation(edge) else "Even"
                x, y, z, a = edge
                f.write(f"{x} {y} {z} {constraint}\n")


def exactly_one(*formulas):
    at_least_one = Or(*formulas)
    at_most_one = And(*[Neg(And(f1, f2))
                        for f1, f2 in itertools.combinations(formulas, 2)])
    return And(at_least_one, at_most_one)

class LatticeC2DislocationLogic:
    def __init__(self, lattice):
        self._lattice = lattice
        self._constraints_formulas = []

        self._add_cell_constraints()
        self._add_edge_constraints()

    def constraints_cnf(self):
        return And(*self._constraints_formulas)

    def _cell_alignment_var(self, cell, alignment):
        v = Atom((cell, alignment))
        v.clausify()
        return v

    def _add_cell_constraints(self):
        for cell in self._lattice.iter_cells():
            self._constrain_cell_single_assignment(cell)

    def _constrain_cell_single_assignment(self, cell):
        cell_alignments_vars = [self._cell_alignment_var(cell, alignment)
                                    for alignment in self._lattice.cell_alignments()]
        # cell_assignment_vars_ids = [a.name for a in cell_alignments_vars]
        # exactly_one = pysat.card.CardEnc.equals(cell_assignment_vars_ids, bound=1, encoding=pysat.card.EncType.pairwise)
        # exactly_one_cnf = CNF(from_clauses=exactly_one.clauses)
        exactly_one_cnf = exactly_one(*cell_alignments_vars)
        self._constraints_formulas.append(exactly_one_cnf)

    def _add_edge_constraints(self):
        for edge in self._lattice.iter_edges():
            if self._lattice.is_dislocation(edge):
                self._constrain_dislocation(edge)
            else:
                self._constrain_normal(edge)

    def _constrain_normal(self, edge):
        adjacent_alignments = self._lattice.edge_adjacent_alignments(edge)
        adjacent_alignment_vars = [self._cell_alignment_var(cell, alignment)
                                    for (cell, alignment) in adjacent_alignments]
        self._constraints_formulas.append(XOr(*adjacent_alignment_vars))

    def _constrain_dislocation(self, edge):
        adjacent_alignments = self._lattice.edge_adjacent_alignments(edge)
        adjacent_alignment_vars = [self._cell_alignment_var(cell, alignment)
                                   for (cell, alignment) in adjacent_alignments]
        # self._constraints_formulas.append(XOr(*adjacent_alignment_vars, PYSAT_TRUE))
        self._constraints_formulas.append(Neg(XOr(*adjacent_alignment_vars)))


def run_realization(lattice_length, random_dislocation_probability):
    lattice = Lattice(lattice_length, lattice_length, lattice_length)
    # TODO: restore
    lattice.generate_dislocation_assignment(random_dislocation_probability)

    sat_rep = LatticeC2DislocationLogic(lattice)

    s = pysat.solvers.Minisat22()
    s.append_formula(sat_rep.constraints_cnf())
    is_sat = s.solve()
    if is_sat:
        print("Solution found")
    else:
        print("No solution")

    lattice.save_to_file('latest_lattice.txt')

def main():
    num_tries = 1
    lattice_length = 4
    probability = 0.1

    probability_percent = str(probability * 100.0)
    print(f"Running {num_tries} realizations of size {lattice_length}x{lattice_length}x{lattice_length} "
          f"with {probability_percent}% random dislocations")

    for i in range(num_tries):
        print("Running realization", i)
        run_realization(lattice_length, probability)

if __name__ == "__main__":
    main()