import argparse

import run_common

from dislocation_structure import Lattice

class C2Lattice(Lattice):
    def __init__(self, x_length, y_length, z_length):
        super().__init__(x_length, y_length, z_length)
        self._alignments = [0, 1, 2]

    def cell_alignments(self):
        return self._alignments

    def edge_adjacent_alignments(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), a),
                    ((x, y + 1, z), a),
                    ((x, y, z + 1), a),
                    ((x, y + 1, z + 1), a)]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), a),
                    ((x + 1, y, z), a),
                    ((x, y, z + 1), a),
                    ((x + 1, y, z + 1), a)]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return [((x, y, z), a),
                ((x + 1, y, z), a),
                ((x, y + 1, z), a),
                ((x + 1, y + 1, z), a)]

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

    run_common.go(C2Lattice(lattice_length, lattice_length, lattice_length),
                  probability, num_tries)

if __name__ == "__main__":
    main()