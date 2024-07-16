import argparse

from c2 import C2Lattice
from z3_logic_engine import Z3LogicEngine
from symbolic_dislocation_logic import SymbolicLatticeDislocationLogic

def main():
    parser = argparse.ArgumentParser(prog='search_c2',
                                     description='Try to find a defect set that cannot be realized')
    parser.add_argument('-l', '--length')

    args = parser.parse_args()
    lattice_length = int(args.length)

    lattice = C2Lattice(lattice_length, lattice_length, lattice_length)
    logic_engine = Z3LogicEngine()
    sat_rep = SymbolicLatticeDislocationLogic(lattice, logic_engine)
    is_sat, defect_set = sat_rep.check_unrealizable_defect_set_existence()
    print(is_sat)
    if is_sat:
        found_lattice = C2Lattice(lattice_length, lattice_length, lattice_length)
        found_lattice.set_defect_set(defect_set)
        found_lattice.save_to_file('unrealizable_lattice.txt')

if __name__ == "__main__":
    main()