import pysat
from pysat.formula import CNF, And, Or, XOr, Neg, Atom, PYSAT_TRUE
import pysat.card
import pysat.solvers

import itertools

class LogicEngine:
    pass

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

    def check_sat(self, formula):
        s = pysat.solvers.Minisat22()
        s.append_formula(formula)
        is_sat = s.solve()
        if not is_sat:
            return False, None
        return True, s.get_model()