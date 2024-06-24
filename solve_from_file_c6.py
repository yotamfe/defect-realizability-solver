import argparse

from c6 import C6Lattice
import run_common

def main():
    parser = argparse.ArgumentParser(prog='solve_from_file_c6',
                                     description='Try to find cell alignments that satisfy '
                                                 'a given dislocation pattern on a lattice')
    parser.add_argument('-i', '--input_file')

    args = parser.parse_args()
    lattice = C6Lattice.load_from_file(args.input_file)

    run_common.run_from_file(lattice)

if __name__ == "__main__":
    main()