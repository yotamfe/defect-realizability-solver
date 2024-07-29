import pydepqbf
from logic_engine import LogicEngine
from pysat_logic_engine import PySATLogicEngine

class DepQBFLogicEngine(LogicEngine):
    def __init__(self):
        self._internal_logic_engine = PySATLogicEngine()

    def var(self, obj):
        return (), self._internal_logic_engine.var(obj)

    def __manipulate_propositional_part(self, args, func):
        quantifiers_lst = [a[0] for a in args]
        assert len(set(quantifiers_lst)) == 1, "Boolean manipulation with different quantifier matrices currently unsupported"
        quantifiers = quantifiers_lst[0]
        propositional_formulas = [a[1] for a in args]
        return (quantifiers, func(*propositional_formulas))

    def And(self, *args):
        return self.__manipulate_propositional_part(args, self._internal_logic_engine.And)

    def Or(self, *args):
        return self.__manipulate_propositional_part(args, self._internal_logic_engine.Or)

    def XOr(self, *args):
        return self.__manipulate_propositional_part(args, self._internal_logic_engine.XOr)

    def XNOr(self, *args):
        return self.__manipulate_propositional_part(args, self._internal_logic_engine.XNOr)

    def exactly_one(self, *formulas):
        return self.__manipulate_propositional_part(formulas, self._internal_logic_engine.exactly_one)

    def Neg(self, arg):
        return self.__manipulate_propositional_part([arg], self._internal_logic_engine.Neg)

    def Eq(self, f1, f2):
        return self.__manipulate_propositional_part([f1, f2], self._internal_logic_engine.Eq)

    def ForAll(self, vars, formula):
        quantifiers = formula[0]
        prop_part = formula[1]
        vars = tuple(v[1].name for v in vars)
        res = (((pydepqbf.QDPLL_QTYPE_FORALL, vars),) + quantifiers, prop_part)
        return res

    def Exists(self, vars, formula):
        quantifiers = formula[0]
        prop_part = formula[1]
        vars = tuple(v[1].name for v in vars)
        res = (((pydepqbf.QDPLL_QTYPE_EXISTS, vars),) + quantifiers, prop_part)
        return res

    def vars_in_formula(self, formula):
        prop_formula = formula[1]
        vars_in_formula = set()
        for clause in prop_formula:
            for lit in clause:
                var = abs(lit)
                vars_in_formula.add(var)
        return vars_in_formula

    def ForAllVarsExcept(self, dont_quantify, formula):
        vars_to_exclude = set(v[1].name for v in dont_quantify)
        vars_to_quantify = self.vars_in_formula(formula) - vars_to_exclude
        print(vars_to_exclude)
        print(vars_to_quantify)
        quantifiers = formula[0]
        prop_part = formula[1]
        res = (((pydepqbf.QDPLL_QTYPE_FORALL, vars_to_quantify),) + quantifiers, prop_part)
        return res

    def ExistAllVarsExcept(self, dont_quantify, formula):
        vars_to_exclude = set(v[1].name for v in dont_quantify)
        vars_to_quantify = self.vars_in_formula(formula) - vars_to_exclude
        print(vars_to_exclude)
        print(vars_to_quantify)
        quantifiers = formula[0]
        prop_part = formula[1]
        res = (((pydepqbf.QDPLL_QTYPE_EXISTS, vars_to_quantify),) + quantifiers, prop_part)
        return res

    def check_sat(self, formula):
        quantifiers, prop_formula = formula
        quantifiers = tuple(quantifiers)
        clauses = self._internal_logic_engine.to_dimacs_repr(prop_formula)
        res, model = pydepqbf.solve(quantifiers, clauses)
        if res == pydepqbf.QDPLL_RESULT_UNSAT:
            return False, None
        if res == pydepqbf.QDPLL_RESULT_SAT:
            return True, model
        assert False, "DepQBF result unknown"

    def var_true_in_model(self, var, model):
        model_set = set(model)
        var_id = int(var[1].name)
        assert var_id in model_set or -var_id in model_set
        return var_id in model_set
