from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from more_itertools import interleave

GRID_WIDTH = 42
GRID_HEIGHT = 7
SPACING = 1  # mm
OFFSET_SPACING = 2.95
NUMBER_OF_ROWS = 2  # x42
NUMBER_OF_COLUMNS = 2  # x42
NUMBER_OF_HEIGHT = 3  # x7 would be 21mm


@dataclass
class Socket:
    height: float
    diameter: float
    name: Optional[str]


class SocketGenerator:
    xy_grid = 42
    z_grid = 7
    _offset_spacing = 2.95

    _cylinder_offset = 1

    def __init__(self, sockets: List[List[Socket]], rows=1, columns=2, height=3):
        self.sockets: List[List[Socket]] = sockets
        self.rows = rows
        self.columns = columns
        self.units_height = height

    @property
    def x_length(self):
        return self.xy_grid * self.columns

    @property
    def y_length(self):
        return self.xy_grid * self.rows

    @property
    def z_offset(self):
        return self.z_grid * self.units_height

    @property
    def box_cutouts(self) -> str:
        x_offset = self._offset_spacing
        y_offset = (
            self._offset_spacing
            + max(s.height for s in self.sockets[0])
            + self._cylinder_offset
        )
        box_y = self.y_length - (self._offset_spacing + y_offset)
        full_width = self.x_length - (self._offset_spacing * 2)
        return f"translate([{x_offset},{y_offset},{self.z_grid}])cube([{full_width:.3f},{box_y:.3f},{(self.z_offset - self.z_grid):.3f}]);"

    @property
    def header_lines(self) -> Iterable[str]:
        return [
            "include <modules/module_gridfinity.scad>",
            "union() {",
            "  difference() {",
            f"  grid_block({self.columns},{self.rows},{self.units_height});",
        ]

    @property
    def socket_lines(self) -> Iterable[str]:
        for sockets in self.sockets:
            spacing = determine_cylinder_spacing(
                self.x_length, [s.diameter for s in sockets], self._offset_spacing
            )
            for i, socket in enumerate(sockets):
                radius = socket.diameter / 2
                trailing = spacing * (1 + i)
                dx = trailing + sum((s.diameter for s in sockets[:i])) + radius
                yield from self.make_cylinder_lines(
                    socket, dx, x_offset=self._offset_spacing, z_offset=self.z_offset
                )

    @property
    def generate_lines(self) -> Iterable[str]:
        yield self.box_cutouts
        yield from self.socket_lines

    def make_text_lines(self):
        for sockets in self.sockets:
            spacing = determine_cylinder_spacing(
                self.x_length, [s.diameter for s in sockets], self._offset_spacing
            )
            for i, socket in enumerate(sockets):
                radius = socket.diameter / 2
                trailing = spacing * (1 + i)
                dx = trailing + sum((s.diameter for s in sockets[:i])) + radius
                yield (f'translate([{dx},{socket.height+5},{self.z_grid}])'
                       'linear_extrude(0.3)'
                       f'text("{socket.name}",size=3, halign="center");')

    def make_cylinder_lines(
        self, socket: Socket, dx, *, x_offset, z_offset
    ) -> Iterable[str]:
        cylinder_lines = ["rotate([90,0,0])", f"translate([0, {z_offset}, 0])"]
        for height, diameter in (
            (socket.height, socket.diameter),
            (socket.height + 3, socket.diameter - 2),
        ):
            yield "".join(
                [
                    *cylinder_lines,
                    f"translate([{dx},0,-{height + x_offset}])",
                    f"cylinder(h={height}, d={diameter});",
                ]
            )

    def write_file(self, path: Path):
        with open(path, "w") as file:
            file.writelines((f"  {line}\n" for line in self.header_lines))
            file.writelines(f"    {line}\n" for line in self.generate_lines)
            file.write("  }\n")
            file.writelines((f" {line}\n" for line in self.make_text_lines()))
            file.write("}")


def determine_cylinder_spacing(
    length: float, cylinders: List[float], min_space: float = OFFSET_SPACING
) -> float:
    """
    Determines the spacing between the sockets based on their diameters.
    The spacing is calculated as the maximum diameter plus a fixed spacing value.
    """
    assert len(cylinders), "The list of diameters cannot be empty."
    num_of_spaces = len(cylinders) + 1
    leftover = length - (sum(cylinders) + min_space * num_of_spaces)
    assert (
        leftover >= 0
    ), f"The sum of diameters exceeds the length. leftover={leftover}"
    delta_leftover = (length - sum(cylinders)) / num_of_spaces
    return delta_leftover


def determine_box_spacing(length: float, number_boxes: int) -> float:
    num_of_spaces = number_boxes + 1
    usable_space = length - (OFFSET_SPACING * num_of_spaces)
    return usable_space / number_boxes


if __name__ == "__main__":

    fn = "main.scad"
    socket_generator = SocketGenerator(
        [
            [
                Socket(height=28.5, diameter=18.35, name="13mm"),
                Socket(height=28.5, diameter=20.35, name="14mm"),
                Socket(height=28.5, diameter=22.25, name="15mm"),
                # Socket(height=26, diameter=20),
                # Socket(height=26, diameter=25),
                # Socket(height=20, diameter=25),
            ],
            # [
            #     Socket(height=26, diameter=10),
            #     Socket(height=26, diameter=15),
            #     Socket(height=26, diameter=20),
            #     Socket(height=26, diameter=25),
            # ],
        ]
    )
    socket_generator.write_file(fn)
