from abc import ABC, abstractmethod

class LogicEngine(ABC):
    @abstractmethod
    def var(self, obj):
        pass

    @abstractmethod
    def And(self, *args):
        pass

    @abstractmethod
    def Or(self, *args):
        pass

    @abstractmethod
    def XOr(self, *args):
        pass

    @abstractmethod
    def XNOr(self, *args):
        pass

    @abstractmethod
    def exactly_one(self, *formulas):
        pass

    @abstractmethod
    def check_sat(self, formula):
        pass

    @abstractmethod
    def var_true_in_model(self, var, model):
        pass
