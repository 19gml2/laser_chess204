
from nnf import And, dsharp, NNF, config


class Encoding(object):
    def __init__(self):
        self.constraints = []

    def vars(self):
        ret = set()
        for c in self.constraints:
            ret |= c.vars()
        return ret

    def size(self):
        ret = 0
        for c in self.constraints:
            ret += c.size()
        return ret

    def valid(self):
        return And(self.constraints).valid()

    def negate(self):
        return And(self.constraints).negate()

    def add_constraint(self, c):
        assert isinstance(c, NNF), "Constraints need to be of type NNF"
        self.constraints.append(c)

    @config(sat_backend="kissat")
    def is_satisfiable(self):
        return And(self.constraints).satisfiable()

    @config(sat_backend="kissat")
    def solve(self):
        return And(self.constraints).solve()

    def count_solutions(self, lits=[]):
        if lits:
            T = And(self.constraints + lits)
        else:
            T = And(self.constraints)

        if not T.satisfiable():
            return 0

        return dsharp.compile(T.to_CNF(), executable='bin/dsharp', smooth=True).model_count()

    def likelihood(self, lit):
        return self.count_solutions([lit]) / self.count_solutions()
