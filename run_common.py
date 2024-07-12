import numpy as np
import itertools

from dislocation_logic import LatticeDislocationLogic
from pysat_logic_engine import PySATLogicEngine

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
    logic_engine = PySATLogicEngine()
    sat_rep = LatticeDislocationLogic(lattice, logic_engine)
    is_sat, cell_assignment = sat_rep.check_realizability()
    if is_sat:
        print("Solution found")
        write_satisfying_assignment(cell_assignment, lattice)
        verify_assignment(lattice, cell_assignment)
    else:
        print("No solution")

def write_satisfying_assignment(cell_assignment, lattice):
    with open("latest_model.txt", "wt") as f:
        for k, v in cell_assignment.items():
            f.write(f"{k} {v}\n")
        f.write("\n")
        for edge in lattice.iter_edges():
            dislocation_expected = "Dislocation" if lattice.is_dislocation(edge) else "Normal"
            f.write(f"{edge}: {dislocation_expected}\n")
            adjacent_alignment_blocks = lattice.edge_adjacent_alignment_blocks(edge)
            for block in adjacent_alignment_blocks:
                truthifying_cells = [(cell, alignment) for (cell, alignment) in block
                                     if cell_assignment[cell] == alignment]
                adjacent_alignments_in_block = [str(alignment) for (cell, alignment) in block]
                if truthifying_cells == []:
                    cells_in_block = [cell for (cell, alignment) in block]
                    assert len(set(cells_in_block)) == 1 # (true for c6 becusae a block always involves just one cell)
                    falsifying_cell = cells_in_block[0]
                    falsifying_assignment = cell_assignment[falsifying_cell]
                    f.write(f"\tFalse:\t{falsifying_cell}={falsifying_assignment}"
                            f"\tnot in\t{adjacent_alignments_in_block}\n")
                else:
                    truthifying_cell, truthifying_alignment = truthifying_cells[0]
                    f.write(f"\tTrue:\t{truthifying_cell}={truthifying_alignment}"
                            f"\tin\t\t{adjacent_alignments_in_block}\n")


def go(lattice, probability, num_tries):
    for i in range(num_tries):
        print("Running realization", i)
        run_realization(lattice, probability)

def run_from_file(lattice):
    solve(lattice)