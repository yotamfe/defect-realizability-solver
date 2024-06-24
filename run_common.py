import numpy as np
import itertools

import pysat
import pysat.solvers

from dislocation_structure import Lattice

def run_realization(lattice_length, random_dislocation_probability, dislocation_logic_factory):
    lattice = Lattice(lattice_length, lattice_length, lattice_length)
    lattice.generate_dislocation_assignment(random_dislocation_probability)

    sat_rep = dislocation_logic_factory(lattice)

    s = pysat.solvers.Minisat22()
    s.append_formula(sat_rep.constraints_cnf())
    is_sat = s.solve()
    if is_sat:
        print("Solution found")
    else:
        print("No solution")

    lattice.save_to_file('latest_lattice.txt')

def go(lattice_length, probability, num_tries, dislocation_logic_factory):
    for i in range(num_tries):
        print("Running realization", i)
        run_realization(lattice_length, probability, dislocation_logic_factory)