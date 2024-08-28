import numpy as np
import itertools

class LatticeDislocationLogic:
    def __init__(self, lattice, logic_engine):
        self._lattice = lattice
        self._logic_engine = logic_engine
        self._constraints_formulas = []

        self._add_cell_constraints()
        self._add_edge_constraints()

    def constraints_cnf(self):
        return self._logic_engine.And(*self._constraints_formulas)

    def _cell_orientation_var(self, cell, orientation):
        return self._logic_engine.var((cell, orientation))

    def _read_logical_assignment(self, model):
        res = dict()
        for cell in self._lattice.iter_cells():
            for orientation in self._lattice.cell_orientations():
                val = self._logic_engine.var_true_in_model(self._cell_orientation_var(cell, orientation), model)
                res[(cell, orientation)] = val
        return res

    def check_realizability(self):
        is_sat, model = self._logic_engine.check_sat(self.constraints_cnf())
        if not is_sat:
            return False, None
        return True, self.read_cell_assignment(model)

    def read_cell_assignment(self, model):
        potentially_conflicting_assingment = self._read_logical_assignment(model)
        res = dict()
        for cell in self._lattice.iter_cells():
            chosen_orientation = set(orientation for orientation in self._lattice.cell_orientations()
                                 if potentially_conflicting_assingment[(cell, orientation)])
            if len(chosen_orientation) > 1:
                raise ValueError("Conflicting assignment for orientation of cell %s" % str(cell))
            orientation = list(chosen_orientation)[0]
            res[cell] = orientation
        return res

    def _add_cell_constraints(self):
        for cell in self._lattice.iter_cells():
            self._constrain_cell_single_assignment(cell)

    def _constrain_cell_single_assignment(self, cell):
        cell_orientations_vars = [self._cell_orientation_var(cell, orientation)
                                for orientation in self._lattice.cell_orientations()]
        exactly_one_cnf = self._logic_engine.exactly_one(*cell_orientations_vars)
        self._constraints_formulas.append(exactly_one_cnf)

    def _add_edge_constraints(self):
        for edge in self._lattice.iter_edges():
            if self._lattice.is_dislocation(edge):
                self._constrain_dislocation(edge)
            else:
                self._constrain_normal(edge)

    def _block_formula(self, adjacency_block):
        adjacent_orientation_vars = [self._cell_orientation_var(cell, orientation)
                                   for (cell, orientation) in adjacency_block]
        return self._logic_engine.Or(*adjacent_orientation_vars)

    def _constrain_normal(self, edge):
        adjacent_orientations_blocks = self._lattice.edge_adjacent_orientation_blocks(edge)
        adjacent_blocks_encoded = [self._block_formula(block) for block in adjacent_orientations_blocks]
        self._constraints_formulas.append(self._logic_engine.XNOr(*adjacent_blocks_encoded))

    def _constrain_dislocation(self, edge):
        adjacent_orientations_blocks = self._lattice.edge_adjacent_orientation_blocks(edge)
        adjacent_blocks_encoded = [self._block_formula(block) for block in adjacent_orientations_blocks]
        self._constraints_formulas.append(self._logic_engine.XOr(*adjacent_blocks_encoded))
