import argparse
from enum import Enum

import run_common
from dislocation_structure import Lattice

class C6CellAlignments(Enum):
    XY = 0
    XZ = 1
    YX = 2
    YZ = 3
    ZX = 4
    ZY = 5

class C6Lattice(Lattice):
    def __init__(self, x_length, y_length, z_length):
        super().__init__(x_length, y_length, z_length)
        self._alignments = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    def cell_alignments(self):
        return self._alignments

    def edge_adjacent_alignments(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), C6CellAlignments.YX),
                    ((x, y, z), C6CellAlignments.ZY),
                    ((x, y + 1, z), C6CellAlignments.YZ),
                    ((x, y + 1, z), C6CellAlignments.ZY),
                    ((x, y, z + 1), C6CellAlignments.YX),
                    ((x, y, z + 1), C6CellAlignments.ZX),
                    ((x, y + 1, z + 1), C6CellAlignments.YZ),
                    ((x, y + 1, z + 1), C6CellAlignments.ZX)]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [((x, y, z), C6CellAlignments.ZY),
                    ((x, y, z), C6CellAlignments.XZ),
                    ((x + 1, y, z), C6CellAlignments.ZX),
                    ((x + 1, y, z), C6CellAlignments.XZ),
                    ((x, y, z + 1), C6CellAlignments.ZY),
                    ((x, y, z + 1), C6CellAlignments.XY),
                    ((x + 1, y, z + 1), C6CellAlignments.ZX),
                    ((x + 1, y, z + 1), C6CellAlignments.XY)]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return [((x, y, z), C6CellAlignments.XZ),
                ((x, y, z), C6CellAlignments.YX),
                ((x + 1, y, z), C6CellAlignments.XY),
                ((x + 1, y, z), C6CellAlignments.YX),
                ((x, y + 1, z), C6CellAlignments.XZ),
                ((x, y + 1, z), C6CellAlignments.YZ),
                ((x + 1, y + 1, z), C6CellAlignments.XY),
                ((x + 1, y + 1, z), C6CellAlignments.YZ)]

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Dislocation" if self.is_dislocation(edge) else "Normal"
                x, y, z, a = edge
                f.write(f"{x} {y} {z} {constraint}\n")

def main():
    parser = argparse.ArgumentParser(prog='run_c6',
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

    run_common.go(C6Lattice(lattice_length, lattice_length, lattice_length),
                  probability, num_tries)

if __name__ == "__main__":
    main()