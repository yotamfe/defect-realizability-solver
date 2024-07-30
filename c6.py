from enum import Enum

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
        self._alignments = [C6CellAlignments.XY, C6CellAlignments.XZ, C6CellAlignments.YX,
                            C6CellAlignments.YZ, C6CellAlignments.ZX, C6CellAlignments.ZY]

    def cell_alignments(self):
        return self._alignments

    def edge_adjacent_alignment_blocks(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [[
                        ((x, y, z), C6CellAlignments.YX),
                        ((x, y, z), C6CellAlignments.ZY)
                    ],
                    [
                        ((x, y + 1, z), C6CellAlignments.YZ),
                        ((x, y + 1, z), C6CellAlignments.ZY)
                    ],
                    [
                        ((x, y, z + 1), C6CellAlignments.YX),
                        ((x, y, z + 1), C6CellAlignments.ZX)
                    ],
                    [
                        ((x, y + 1, z + 1), C6CellAlignments.YZ),
                        ((x, y + 1, z + 1), C6CellAlignments.ZX)
                    ]]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [[
                        ((x, y, z), C6CellAlignments.ZY),
                        ((x, y, z), C6CellAlignments.XY)
                    ],
                    [
                        ((x + 1, y, z), C6CellAlignments.ZX),
                        ((x + 1, y, z), C6CellAlignments.XZ)
                    ],
                    [
                        ((x, y, z + 1), C6CellAlignments.ZY),
                        ((x, y, z + 1), C6CellAlignments.XY)
                    ],
                    [
                        ((x + 1, y, z + 1), C6CellAlignments.ZX),
                        ((x + 1, y, z + 1), C6CellAlignments.XZ)
                    ]]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return [[
                    ((x, y, z), C6CellAlignments.XZ),
                    ((x, y, z), C6CellAlignments.YX)
                ],
                [
                    ((x + 1, y, z), C6CellAlignments.XY),
                    ((x + 1, y, z), C6CellAlignments.YX)
                ],
                [
                    ((x, y + 1, z), C6CellAlignments.XZ),
                    ((x, y + 1, z), C6CellAlignments.YZ)
                ],
                [
                    ((x + 1, y + 1, z), C6CellAlignments.XY),
                    ((x + 1, y + 1, z), C6CellAlignments.YZ)
                ]]

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Dislocation" if self.is_dislocation(edge) else "Normal"
                x, y, z, a = edge
                f.write(f"{x} {y} {z} {constraint}\n")

    @staticmethod
    def load_from_file(path):
        with open(path, "rt") as f:
            line = f.readline().strip()
            if len(line.split()) != 3:
                raise ValueError("Malformed file: Expecting first line lattice size {x length} {y length} {z length}")
            x_length_str, y_length_str, z_length_str = line.split()
            x_length, y_length, z_length = int(x_length_str), int(y_length_str), int(z_length_str)
            if not (x_length > 0 and y_length > 0 and z_length > 0):
                raise InputException(
                    "Malformed file: Expecting positive lattice sizes {x length} {y length} {z length}")

            lattice = C6Lattice(int(x_length_str), int(y_length_str), int(z_length_str))

            for edge in lattice.iter_edges():
                expect_x, expect_y, expect_z, expect_a = edge
                line = f.readline()
                if len(line.split()) != 4:
                    raise ValueError("Malformed file: expecting {x} {y} {z} {Odd/Even}")
                x_str, y_str, z_str, disloc_str = line.split()
                if int(x_str) != expect_x or int(y_str) != expect_y or int(z_str) != expect_z:
                    raise ValueError(f"Malformed file: expecting edge {expect_x} {expect_y} {expect_z} {expect_a}"
                                     f"got {x_str} {y_str} {z_str}")
                if disloc_str == "Dislocation":
                    lattice._dislocations_edgeset.add(edge)
                elif disloc_str != "Normal":
                    raise ValueError(
                        f"Malformed file: unknown dislocation status for line {x_str} {y_str} {z_str} {disloc_str}")

            return lattice