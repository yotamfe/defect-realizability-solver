import numpy as np
import itertools

from pysat.formula import CNF, And, Or, XOr, Neg, Atom, PYSAT_TRUE
import pysat.card

def exactly_one(*formulas):
    at_least_one = Or(*formulas)
    at_most_one = And(*[Neg(And(f1, f2))
                        for f1, f2 in itertools.combinations(formulas, 2)])
    return And(at_least_one, at_most_one)

class LatticeDislocationLogic:
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

    def _read_logical_assignment(self, model):
        model_set = set(model)
        res = dict()
        for cell in self._lattice.iter_cells():
            for alignment in self._lattice.cell_alignments():
                val = self._cell_alignment_var(cell, alignment).name in model_set
                res[(cell, alignment)] = val
        return res

    def read_cell_assignment(self, model):
        potentially_conflicting_assingment = self._read_logical_assignment(model)
        res = dict()
        for cell in self._lattice.iter_cells():
            chosen_alignments = set(alignment for alignment in self._lattice.cell_alignments()
                                 if potentially_conflicting_assingment[(cell, alignment)])
            if len(chosen_alignments) > 1:
                raise ValueError("Conflicting assignment for orientation of cell %s" % str(cell))
            alignment = list(chosen_alignments)[0]
            res[cell] = alignment
        return res

    def _add_cell_constraints(self):
        for cell in self._lattice.iter_cells():
            self._constrain_cell_single_assignment(cell)

    def _constrain_cell_single_assignment(self, cell):
        cell_alignments_vars = [self._cell_alignment_var(cell, alignment)
                                    for alignment in self._lattice.cell_alignments()]
        # TODO: try pysat's cardinality encoding
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
        # TODO: try xor with true
        # self._constraints_formulas.append(XOr(*adjacent_alignment_vars, PYSAT_TRUE))
        self._constraints_formulas.append(Neg(XOr(*adjacent_alignment_vars)))

    def _constrain_dislocation(self, edge):
        adjacent_alignments = self._lattice.edge_adjacent_alignments(edge)
        adjacent_alignment_vars = [self._cell_alignment_var(cell, alignment)
                                   for (cell, alignment) in adjacent_alignments]
        self._constraints_formulas.append(XOr(*adjacent_alignment_vars))

