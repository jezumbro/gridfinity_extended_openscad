import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

GRID_WIDTH = 42
GRID_HEIGHT = 7
SPACING = 1  # mm
NUMBER_OF_ROWS = 2  # x42
NUMBER_OF_COLUMNS = 2  # x42
NUMBER_OF_HEIGHT = 3  # x7 would be 21mm


@dataclass
class Socket:
    height: float
    diameter: float
    name: Optional[str]

    @property
    def radius(self) -> float:
        return self.diameter / 2


class SocketGenerator:
    xy_grid = 42
    z_grid = 7
    _offset_spacing = 2.9

    _cylinder_offset = 0.8

    def __init__(self, sockets: List[List[Socket]]):
        self.sockets: List[List[Socket]] = sockets
        self.rows = math.ceil(
            max(s.height for socket in sockets for s in socket) / self.xy_grid
        )
        self.columns = math.ceil(
            sum(s.diameter for socket in sockets for s in socket) / self.xy_grid
        )
        self.units_height = (
            math.ceil(max(s.radius for socket in sockets for s in socket) / self.z_grid)
            + 1
        )

    @property
    def x_length(self):
        return self.xy_grid * self.columns

    @property
    def y_length(self):
        return self.xy_grid * self.rows

    @property
    def z_length(self):
        return self.z_grid * self.units_height

    @property
    def max_socket_radius(self):
        return max(s.radius for sockets in self.sockets for s in sockets)

    @property
    def box_cutouts(self) -> str:
        x_offset = self._offset_spacing
        y_offset = (
            self._offset_spacing
            + max(s.height for s in self.sockets[0])
            + self._cylinder_offset
        )
        z_offset = self.z_length - self.max_socket_radius
        box_y = self.y_length - (self._offset_spacing + y_offset)
        full_width = self.x_length - (self._offset_spacing * 2)
        box_z = (self.z_length - z_offset) + 1
        return f"translate([{x_offset:.3f},{y_offset:.3f},{z_offset:.3f}])cube([{full_width:.3f},{box_y:.3f},{box_z :.3f}]);"

    @property
    def header_lines(self) -> Iterable[str]:
        return [
            "include <modules/module_gridfinity.scad>",
            "$fn=64;",
            "difference() {",
            f'grid_block({self.columns},{self.rows},{self.units_height},lip_settings=LipSettings(lipStyle="none"));',
        ]

    @property
    def socket_lines(self) -> Iterable[str]:
        for sockets in self.sockets:
            spacing = determine_cylinder_spacing(
                self.x_length - 2 * self._offset_spacing,
                [s.diameter for s in sockets],
                self._offset_spacing,
            )
            for i, socket in enumerate(sockets):
                trailing = spacing * i + self._offset_spacing
                dx = trailing + sum((s.diameter for s in sockets[:i])) + socket.radius
                yield (
                    f"translate([{dx:.3f},{socket.height/2 + self._offset_spacing:.3f},{(self.z_length - socket.radius - 0.5):.3f}])"
                    "rotate([0,0,270])"
                    f'linear_extrude(5)text("{socket.name}",size=6,halign="center",valign="center");'
                )
                yield from self.make_cylinder_lines(
                    socket, dx, x_offset=self._offset_spacing, z_offset=self.z_length
                )

    @property
    def generate_lines(self) -> Iterable[str]:
        yield self.box_cutouts
        yield from self.socket_lines

    def make_cylinder_lines(
        self, socket: Socket, dx, *, x_offset, z_offset
    ) -> Iterable[str]:
        cylinder_lines = ["rotate([90,0,0])", f"translate([0, {z_offset:.3f}, 0])"]
        for height, diameter in (
            (socket.height, socket.diameter),
            (socket.height + self._cylinder_offset + 1, socket.diameter - 2),
        ):
            yield "".join(
                [
                    *cylinder_lines,
                    f"translate([{dx:.3f},0,-{(height + x_offset):.3f}])",
                    f"cylinder(h={height:.3f}, d={diameter:.3f});",
                ]
            )

    def write_file(self, path: Path):
        with open(path, "w") as file:
            file.writelines(
                f"  {line}\n"
                for line in (
                    *self.header_lines,
                    *self.generate_lines,
                )
            )
            file.write("}")


def determine_cylinder_spacing(
    length: float, cylinders: List[float], min_space: float
) -> float:
    """
    Determines the spacing between the sockets based on their diameters.
    The spacing is calculated as the maximum diameter plus a fixed spacing value.
    """
    assert len(cylinders) > 1, "The list of diameters cannot be empty."
    num_of_spaces = len(cylinders) - 1
    leftover = length - (sum(cylinders) + min_space * num_of_spaces)
    assert (
        leftover >= 0
    ), f"The sum of diameters exceeds the length. leftover={leftover}"
    delta_leftover = (length - sum(cylinders)) / num_of_spaces
    return delta_leftover


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
