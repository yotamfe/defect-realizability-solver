import argparse

from c6 import C6Lattice
import run_common

def main():
    parser = argparse.ArgumentParser(prog='solve_from_file_c6',
                                     description='Try to find cell orientations that satisfy '
                                                 'a given defect set on a lattice')
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-s', '--solver',
                        choices=['minisat', 'z3'],
                        default='minisat')

    args = parser.parse_args()
    lattice = C6Lattice.load_from_file(args.input_file)

    run_common.run_from_file(lattice, args.solver)

if __name__ == "__main__":
    main()