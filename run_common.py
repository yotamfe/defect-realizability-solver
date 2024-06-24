import numpy as np
import itertools

import pysat
import pysat.solvers

from dislocation_logic import LatticeDislocationLogic

def run_realization(lattice, random_dislocation_probability):
    lattice.generate_dislocation_assignment(random_dislocation_probability)

    sat_rep = LatticeDislocationLogic(lattice)

    s = pysat.solvers.Minisat22()
    s.append_formula(sat_rep.constraints_cnf())
    is_sat = s.solve()
    if is_sat:
        print("Solution found")
    else:
        print("No solution")

    lattice.save_to_file('latest_lattice.txt')

def go(lattice, probability, num_tries):
    for i in range(num_tries):
        print("Running realization", i)
        run_realization(lattice, probability)