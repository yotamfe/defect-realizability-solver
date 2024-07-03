import numpy as np
import itertools

import pysat
import pysat.solvers

from dislocation_logic import LatticeDislocationLogic

def run_realization(lattice, random_dislocation_probability):
    lattice.generate_dislocation_assignment(random_dislocation_probability)

    solve(lattice)

    lattice.save_to_file('latest_lattice.txt')

def verify_assignment(lattice, cell_assignment):
    for edge in lattice.iter_edges():
        adjacent_alignment_blocks = lattice.edge_adjacent_alignment_blocks(edge)
        blocks = [any(cell_assignment[cell] == alignment for (cell, alignment) in block)
                    for block in adjacent_alignment_blocks]
        edge_parity = len([b for b in blocks if b]) % 2
        if lattice.is_dislocation(edge):
            assert edge_parity != 0, "Expected dislocation in edge %s but found even number adjacent" % edge
        else:
            assert edge_parity == 0, "Expected normal in edge %s but found odd number adjacent" % edge

def solve(lattice):
    sat_rep = LatticeDislocationLogic(lattice)
    s = pysat.solvers.Minisat22()
    s.append_formula(sat_rep.constraints_cnf())
    is_sat = s.solve()
    if is_sat:
        print("Solution found")
        cell_assignment = sat_rep.read_cell_assignment(s.get_model())
        for k, v in cell_assignment.items():
            print(k, v)
        verify_assignment(lattice, cell_assignment)
    else:
        print("No solution")


def go(lattice, probability, num_tries):
    for i in range(num_tries):
        print("Running realization", i)
        run_realization(lattice, probability)

def run_from_file(lattice):
    solve(lattice)