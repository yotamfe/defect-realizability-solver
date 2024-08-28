from defect_structure import Lattice

class C2Lattice(Lattice):
    def __init__(self, x_length, y_length, z_length):
        super().__init__(x_length, y_length, z_length)
        self._orientations = [0, 1, 2]

    def cell_orientations(self):
        return self._orientations

    def edge_adjacent_orientation_blocks(self, edge):
        x, y, z, a = edge
        if a == 0:
            assert y < self._y_length - 1
            assert z < self._z_length - 1
            return [[((x, y, z), a)],
                    [((x, y + 1, z), a)],
                    [((x, y, z + 1), a)],
                    [((x, y + 1, z + 1), a)]]
        if a == 1:
            assert x < self._x_length - 1
            assert z < self._z_length - 1
            return [[((x, y, z), a)],
                    [((x + 1, y, z), a)],
                    [((x, y, z + 1), a)],
                    [((x + 1, y, z + 1), a)]]
        assert a == 2
        assert x < self._x_length - 1
        assert y < self._y_length - 1
        return [[((x, y, z), a)],
                [((x + 1, y, z), a)],
                [((x, y + 1, z), a)],
                [((x + 1, y + 1, z), a)]]

    def save_to_file(self, path):
        with open(path, "wt") as f:
            f.write(f"{self._x_length} {self._y_length} {self._z_length}\n")
            for edge in self.iter_edges():
                constraint = "Odd" if self.is_defect(edge) else "Even"
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

            lattice = C2Lattice(int(x_length_str), int(y_length_str), int(z_length_str))

            for edge in lattice.iter_edges():
                expect_x, expect_y, expect_z, expect_a = edge
                line = f.readline()
                if len(line.split()) != 4:
                    raise ValueError("Malformed file: expecting {x} {y} {z} {Odd/Even}")
                x_str, y_str, z_str, defect_str = line.split()
                if int(x_str) != expect_x or int(y_str) != expect_y or int(z_str) != expect_z:
                    raise ValueError(f"Malformed file: expecting edge {expect_x} {expect_y} {expect_z} {expect_a}"
                                         f"got {x_str} {y_str} {z_str}")
                if defect_str == "Odd":
                    lattice._defects_edgeset.add(edge)
                elif defect_str != "Even":
                    raise ValueError(f"Malformed file: unknown defect status for line {x_str} {y_str} {z_str} {defect_str}")

            return lattice

