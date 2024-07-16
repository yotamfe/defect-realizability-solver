import itertools
import functools

import z3
from z3 import And, Or, Not, Xor, Bool, Solver, ForAll

from logic_engine import LogicEngine

class Z3LogicEngine(LogicEngine):
    def var(self, obj):
        v = Bool(str(obj))
        return v

    def And(self, *args):
        return And(*args)

    def Or(self, *args):
        return Or(*args)

    def XOr(self, *args):
        return functools.reduce(Xor, args)

    def XNOr(self, *args):
        return Not(self.XOr(*args))

    def Neg(self, arg):
        return Not(arg)

    def exactly_one(self, *formulas):
        # TODO: try Z3's AtMost and AtLeast
        at_least_one = Or(*formulas)
        at_most_one = And(*[Not(And(f1, f2))
                            for f1, f2 in itertools.combinations(formulas, 2)])
        return And(at_least_one, at_most_one)

    def Eq(self, f1, f2):
        return f1 == f2

    def ForAll(self, vars, formula):
        return ForAll(vars, formula)

    def check_sat(self, formula):
        s = Solver()
        s.add(formula)
        res = s.check()
        assert res in [z3.sat, z3.unsat], res
        if res == z3.unsat:
            return False, None
        return True, s.model()

    def var_true_in_model(self, var, model):
        return model[var]