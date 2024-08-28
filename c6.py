from enum import Enum

from defect_structure import Lattice

class C6CellOrientations(Enum):
    XY = 0
    XZ = 1
    YX = 2
    YZ = 3
    ZX = 4
    ZY = 5

class C6Lattice(Lattice):
    def __init__(self, x_length, y_length, z_length):
        super().__init__(x_length, y_length, z_length)
        self._orientations = [C6CellOrientations.XY, C6CellOrientations.XZ, C6CellOrientations.YX,
                              C6CellOrientations.YZ, C6CellOrientations.ZX, C6CellOrientations.ZY]

    def cell_orientations(self):
        return self._orientations

    def edge_adjacent_orientation_blocks(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [[
                        ((x, y + 1, z), C6CellOrientations.ZX),
                        ((x, y + 1, z), C6CellOrientations.YZ)
                    ],
                    [
                        ((x, y, z), C6CellOrientations.ZX),
                        ((x, y, z), C6CellOrientations.YX)
                    ],
                    [
                        ((x, y + 1, z + 1), C6CellOrientations.ZY),
                        ((x, y + 1, z + 1), C6CellOrientations.YZ)
                    ],
                    [
                        ((x, y, z + 1), C6CellOrientations.ZY),
                        ((x, y, z + 1), C6CellOrientations.YX)
                    ]]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [[
                        ((x, y, z), C6CellOrientations.ZY),
                        ((x, y, z), C6CellOrientations.XY)
                    ],
                    [
                        ((x + 1, y, z), C6CellOrientations.ZY),
                        ((x + 1, y, z), C6CellOrientations.XZ)
                    ],
                    [
                        ((x, y, z + 1), C6CellOrientations.ZX),
                        ((x, y, z + 1), C6CellOrientations.XY)
                    ],
                    [
                        ((x + 1, y, z + 1), C6CellOrientations.ZX),
                        ((x + 1, y, z + 1), C6CellOrientations.XZ)
                    ]]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return [[
                    ((x, y, z), C6CellOrientations.YZ),
                    ((x, y, z), C6CellOrientations.XZ)
                ],
                [
                    ((x + 1, y, z), C6CellOrientations.YZ),
                    ((x + 1, y, z), C6CellOrientations.XY)
                ],
                [
                    ((x, y + 1, z), C6CellOrientations.YX),
                    ((x, y + 1, z), C6CellOrientations.XZ)
                ],
                [
                    ((x + 1, y + 1, z), C6CellOrientations.YX),
                    ((x + 1, y + 1, z), C6CellOrientations.XY)
                ]]

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Dislocation" if self.is_defect(edge) else "Normal"
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
                    lattice._defects_edgeset.add(edge)
                elif disloc_str != "Normal":
                    raise ValueError(
                        f"Malformed file: unknown defect status for line {x_str} {y_str} {z_str} {disloc_str}")

            return lattice
