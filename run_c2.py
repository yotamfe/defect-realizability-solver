import argparse

from dislocation_logic import LatticeC2DislocationLogic
import run_common

def main():
    parser = argparse.ArgumentParser(prog='run_c2',
                                     description='Try to find cell alignments that satisfy '
                                                 'a random dislocation pattern on a lattice')
    parser.add_argument('-l', '--length')
    parser.add_argument('-n', '--num_tries')
    parser.add_argument('-p', '--probability')

    args = parser.parse_args()
    lattice_length = int(args.length)
    probability = float(args.probability)
    num_tries = int(args.num_tries)

    probability_percent = str(probability * 100.0)
    print(f"Running {num_tries} realizations of size {lattice_length}x{lattice_length}x{lattice_length} "
          f"with {probability_percent}% random dislocations")

    run_common.go(lattice_length, probability, num_tries,
                  lambda lattice: LatticeC2DislocationLogic(lattice))

if __name__ == "__main__":
    main()