from dislocation_logic import LatticeDislocationLogic

class SymbolicLatticeDislocationLogic(LatticeDislocationLogic):

    def _is_defect_symbolic_var_name(self, edge):
        return ('defect', edge)

    def _is_defect_symbolic_var(self, edge):
        return self._logic_engine.var(self._is_defect_symbolic_var_name(edge))

    def _add_edge_constraints(self):
        for edge in self._lattice.iter_edges():
            self._constrain_dislocation_symbolic(edge)

    def _constrain_dislocation_symbolic(self, edge):
        adjacent_alignments_blocks = self._lattice.edge_adjacent_alignment_blocks(edge)
        adjacent_blocks_encoded = [self._block_formula(block) for block in adjacent_alignments_blocks]
        self._constraints_formulas.append(self._logic_engine.Eq(self._is_defect_symbolic_var(edge),
                                                                self._logic_engine.XOr(*adjacent_blocks_encoded)))

    def constrain_even_num_dislocations_per_cell(self):
        constaints = []
        for cell in self._lattice._iter_internal_cells(): # TODO: make public
            cell_edges = self._lattice._cell_edges(cell)
            cell_edges_defected_variables = [self._is_defect_symbolic_var(edge) for edge in cell_edges]
            constraint = self._logic_engine.XNOr(*cell_edges_defected_variables)
            constaints.append(constraint)
        return self._logic_engine.And(*constaints)

    def forall_cell_alignments(self, formula):
        cell_vars = [self._cell_alignment_var(cell, alignment)
                     for cell in self._lattice.iter_cells()
                     for alignment in self._lattice.cell_alignments()]
        return self._logic_engine.ForAll(cell_vars,
                                         formula)

    def exists_defect_set(self, formula):
        is_defect_vars = [self._is_defect_symbolic_var(edge)
                            for edge in self._lattice.iter_edges()]
        return self._logic_engine.Exists(is_defect_vars,
                                         formula)

    def forall_defect_set(self, formula):
        is_defect_vars = [self._is_defect_symbolic_var(edge)
                            for edge in self._lattice.iter_edges()]
        return self._logic_engine.ForAll(is_defect_vars,
                                         formula)

    def forall_non_edge_defect_vars(self, formula):
        is_defect_vars = set(self._is_defect_symbolic_var(edge)
                          for edge in self._lattice.iter_edges())
        return self._logic_engine.ForAllVarsExcept(is_defect_vars, formula)

    def exists_non_edge_defect_vars(self, formula):
        is_defect_vars = set(self._is_defect_symbolic_var(edge)
                          for edge in self._lattice.iter_edges())
        return self._logic_engine.ExistAllVarsExcept(is_defect_vars, formula)

    def _read_edge_defect_logical_assignment(self, model):
        res = dict()
        for edge in self._lattice.iter_edges():
            val = self._logic_engine.var_true_in_model(self._is_defect_symbolic_var(edge), model)
            res[edge] = val
        return res

    def read_defect_set(self, model):
        assignment = self._read_edge_defect_logical_assignment(model)
        res = set()
        for edge in self._lattice.iter_edges():
            if edge not in assignment:
                res.add(edge) # TODO: non-internal edges always defected?
                continue
            if assignment[edge]:
                res.add(edge)
        return res

    def check_unrealizable_defect_set_existence(self):
        # TODO: careful about auxiliary variables from Tsietin encoding!
        # formula = self.forall_cell_alignments(self._logic_engine.And(self.constrain_even_num_dislocations_per_cell(),
        #                                                             self._logic_engine.Neg(self.constraints_cnf())))
        # formula = self.exists_defect_set(self.forall_cell_alignments(self._logic_engine.Neg(self.constraints_cnf())))
        # formula = self.forall_cell_alignments(self._logic_engine.Neg(self.constraints_cnf()))
        # formula = self.forall_non_edge_defect_vars(self._logic_engine.Neg(self.constraints_cnf()))
        # formula = self.exists_defect_set(self.forall_non_edge_defect_vars(self._logic_engine.Neg(self.constraints_cnf())))
        # is_sat, model = self._logic_engine.check_sat(formula)
        # if not is_sat:
        #     return False, None
        # return True, self.read_defect_set(model)
        formula = self.forall_defect_set(self.exists_non_edge_defect_vars(self._logic_engine.Or(self.constraints_cnf(),
                                                                                                self._logic_engine.Neg(self.constrain_even_num_dislocations_per_cell()))))
        is_sat, model = self._logic_engine.check_sat(formula)
        if is_sat:
            return False, None
        return True, self.read_defect_set(model)

