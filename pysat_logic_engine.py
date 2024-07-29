import itertools

import pysat
from pysat.formula import CNF, And, Or, XOr, Neg, Equals, Atom, PYSAT_TRUE
import pysat.card
import pysat.solvers

from logic_engine import LogicEngine
class PySATLogicEngine(LogicEngine):
    def var(self, obj):
        v = Atom(obj)
        v.clausify()
        return v

    def And(self, *args):
        return And(*args)

    def Or(self, *args):
        return Or(*args)

    def XOr(self, *args):
        return XOr(*args)

    def XNOr(self, *args):
        return Neg(XOr(*args))

    def exactly_one(self, *formulas):
        # TODO: try pysat's cardinality encoding
        # cell_assignment_vars_ids = [a.name for a in cell_alignments_vars]
        # exactly_one = pysat.card.CardEnc.equals(cell_assignment_vars_ids, bound=1, encoding=pysat.card.EncType.pairwise)
        # exactly_one_cnf = CNF(from_clauses=exactly_one.clauses)
        at_least_one = Or(*formulas)
        at_most_one = And(*[Neg(And(f1, f2))
                            for f1, f2 in itertools.combinations(formulas, 2)])
        return And(at_least_one, at_most_one)

    def Neg(self, arg):
        return Neg(arg)

    def Eq(self, f1, f2):
        return Equals(f1, f2)

    def to_dimacs_repr(self, formula):
        # from pysat.formula import Formula
        #
        # print(list(Formula._vpool[Formula._context].id2obj.items()))
        # assert False
        # formula.clausify()
        # clauses = formula.clauses
        # for clause in formula.clauses:
        #     for lit in clause:
        #         if clauses == [[lit]]:
        #             # atom - otherwise atom considered a subformula of itself
        #             return clauses
        #         if lit < 0:
        #             # negation proceeds with the positive occurrence of the literal - otherwise infinite loop
        #             lit = -lit
        #         subformulas = formula.formulas([lit], atoms_only=False)
        #         assert len(subformulas) == 1
        #         subformula = subformulas[0]
        #         clauses += self.to_dimacs_repr(subformula)
        # return clauses
        clauses = []
        for clause in formula:
            clauses.append(clause)
        return clauses

    def check_sat(self, formula):
        s = pysat.solvers.Minisat22()
        s.append_formula(formula)
        is_sat = s.solve()
        if not is_sat:
            return False, None
        return True, s.get_model()

    def var_true_in_model(self, var, model):
        model_set = set(model)
        return var.name in model_set
