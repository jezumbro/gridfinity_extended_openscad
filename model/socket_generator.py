import math
from pathlib import Path
from typing import Iterable, List, Optional

from loguru import logger
from more_itertools.more import first, last

from model.configuration import Configuration
from model.socket import MultiLevelSocket, Socket


class SocketGenerator:
    xy_grid = 42
    z_grid = 7
    _offset_spacing = 2.9
    _stackable: bool
    _cylinder_offset = 1.6

    def __init__(
        self,
        sockets: List[List[MultiLevelSocket | Socket]],
        *,
        configuration: Configuration,
    ):
        for row in sockets:

            max_height = max(s.height for s in row) + configuration.tolerance.height
            for socket in row:
                if not configuration.per_item_height:
                    socket.height = max_height
                else:
                    socket.height += configuration.tolerance.height
                socket.add_diameter_tolerance(configuration.tolerance.diameter)
        self.sockets = sockets
        self._rows = configuration.rows
        self._columns = configuration.columns
        self._height = configuration.height
        self._stackable = configuration.stackable
        all_sockets = [s for row in sockets for s in row]
        if len(all_sockets) != set(all_sockets):
            logger.warning("WARN: duplicate sockets found!")
        logger.info(
            f"starting with gridBox({self.rows},{self.columns},{self.stackable_height})"
        )

    @property
    def x_length(self):
        return self.xy_grid * self.columns

    @property
    def y_length(self):
        return self.xy_grid * self.rows

    @property
    def z_length(self):
        return self.z_grid * self.height

    @property
    def columns(self):
        if v := self._columns:
            return v
        max_value = 0
        for row in self.sockets:
            value = math.ceil(
                (sum(s.diameter for s in row) + len(row) - 1) / self.xy_grid
            )
            max_value = max(max_value, value)
        self._columns = max_value
        return self._columns

    @property
    def rows(self):
        if v := self._rows:
            return v
        self._rows = math.ceil(
            max(s.height for row in self.sockets for s in row) / self.xy_grid
        )
        return self._rows

    @property
    def socket_max_radius(self):
        return max(s.radius for row in self.sockets for s in row)

    @property
    def socket_max_diameter(self):
        return max(s.diameter for row in self.sockets for s in row)

    @property
    def height(self):
        return math.ceil((self.socket_max_radius + self.z_grid) / self.z_grid)

    @property
    def stackable_height(self):
        if h := self._height:
            return h
        if self._stackable:
            return math.ceil((self.socket_max_diameter + 2 * self.z_grid) / self.z_grid)
        return math.ceil((self.socket_max_radius + self.z_grid) / self.z_grid)

    @property
    def make_box_cutouts(self) -> str:
        x_offset = self._offset_spacing
        z_offset = self.z_length - self.socket_max_radius
        box_z = (self.z_length - z_offset) + 1
        full_width = self.x_length - (self._offset_spacing * 2)

        row = first(self.sockets)
        y_offset = (
            self._offset_spacing + max(s.height for s in row) + self._cylinder_offset
        )
        box_y = self.y_length - (self._offset_spacing + y_offset)
        if len(self.sockets) > 1:
            row = last(self.sockets)
            box_y -= max(s.height for s in row) + self._cylinder_offset
        return f"translate([{x_offset:.3f},{y_offset:.3f},{z_offset:.3f}])cube([{full_width:.3f},{box_y:.3f},{box_z :.3f}]);"

    @property
    def make_header_lines(self) -> Iterable[str]:
        double_offset = self._offset_spacing * 2
        grid_block_line = (
            f"grid_block({self.columns},{self.rows},{self.stackable_height}"
        )
        yield from [
            "include <modules/module_gridfinity.scad>",
            "$fn=64;",
            "",
            "difference() {",
        ]
        if not self._stackable:
            grid_block_line += ',lip_settings=LipSettings(lipStyle="none")'
        grid_block_line += ");"
        yield grid_block_line
        yield ""
        yield (
            f"translate([{self._offset_spacing:.3f},{self._offset_spacing:.3f},{self.z_length:.3f}])"
            f"cube([{self.x_length-double_offset:.3f},{self.y_length-double_offset:.3f},{2*self.z_length:.3f}]);"
        )

    @property
    def socket_lines(self) -> Iterable[str]:
        for row_index, row in enumerate(self.sockets):
            spacing = self.determine_cylinder_spacing(
                self.x_length - 2 * self._offset_spacing,
                [s.diameter for s in row],
                1,
            )
            logger.info(f"\trow #{row_index+1} spacing: {spacing:.3f}")
            for i, socket in enumerate(row):
                trailing = spacing * i + self._offset_spacing
                dx = trailing + sum((s.diameter for s in row[:i])) + socket.radius
                dy = socket.height / 2 + self._offset_spacing
                if row_index:
                    dy = self.y_length - (socket.height / 2 + self._offset_spacing)
                yield (
                    f"translate([{dx:.3f},{dy:.3f},{(self.z_length - socket.radius - 0.5):.3f}])"
                    "rotate([0,0,270])"
                    f'linear_extrude({self.z_length-socket.radius})text("{socket.name}",size=6,halign="center",valign="center");'
                )
                yield from self.make_cylinder_lines(socket, dx, bool(row_index))

    @property
    def make_all_lines(self) -> Iterable[str]:
        yield self.make_box_cutouts
        yield ""
        yield "// start cylinder lines"
        yield from self.socket_lines

    def make_cylinder_lines(
        self, socket: Socket | MultiLevelSocket, dx, mirror: bool
    ) -> Iterable[str]:
        offset = self._offset_spacing
        if mirror:
            offset = self.y_length - self._offset_spacing
        if func := self.operations[type(socket)]:
            return func(
                socket,
                cylinder_offset=self._cylinder_offset,
                dx=dx,
                offset=offset,
                z_offset=self.z_length,
                mirror=mirror,
            )
        raise ValueError(
            f"unable to generate cylinder lines based on type={type(socket)}"
        )

    def write_file(self, path: Path):
        with open(path, "w") as file:
            file.writelines(
                f"  {line}\n"
                for line in (
                    *self.make_header_lines,
                    *self.make_all_lines,
                )
            )
            file.write("}")

    @staticmethod
    def generate_socket_lines(
        socket: Socket,
        *,
        cylinder_offset: float,
        dx: float,
        offset: float,
        z_offset: float,
        mirror: bool,
    ) -> Iterable[str]:
        yield f"// {socket.name}"
        cylinder_lines = ["rotate([90,0,0])", f"translate([0, {z_offset:.3f}, 0])"]
        extended_cylinder = socket.height + cylinder_offset + 4
        items = (
            (socket.height, socket.diameter, socket.height + offset),
            (extended_cylinder, socket.diameter - 4, extended_cylinder + offset),
        )
        if mirror:
            items = (
                (
                    socket.height,
                    socket.diameter,
                    offset,
                ),
                (
                    extended_cylinder,
                    socket.diameter - 4,
                    extended_cylinder + offset - extended_cylinder,
                ),
            )
        for height, diameter, dy in items:
            yield "".join(
                (
                    *cylinder_lines,
                    f"translate([{dx:.3f},0,-{dy:.3f}])",
                    f"#cylinder(h={height:.3f}, d={diameter:.3f});",
                )
            )

    @staticmethod
    def generate_multi_level_socket_lines(
        socket: MultiLevelSocket,
        *,
        cylinder_offset: float,
        dx: float,
        offset: float,
        z_offset: float,
        mirror: bool,
    ) -> Iterable[str]:
        yield f"// {socket.name}"
        cylinder_lines = ["#rotate([90,0,0])", f"translate([0, {z_offset:.3f}, 0])"]
        dy = socket.offset + offset + socket.transition_length
        if mirror:
            dy = offset - socket.offset
        yield "".join(
            [
                "",
                *cylinder_lines,
                f"translate([{dx:.3f},0,-{dy:.3f}])",
                (
                    f"cylinder(h={socket.transition_length:.3f}, d1={socket.diameter:.3f}, d2={socket.small_diameter:.3f});"
                    if mirror
                    else f"cylinder(h={socket.transition_length:.3f}, d1={socket.small_diameter:.3f}, d2={socket.diameter:.3f});"
                ),
            ]
        )
        extended_cylinder = socket.height + cylinder_offset + 4

        items = (
            (socket.offset, socket.diameter, socket.offset + offset),
            (socket.height, socket.small_diameter, socket.height + offset),
            (
                extended_cylinder,
                socket.small_diameter - 4,
                extended_cylinder + offset,
            ),
        )
        if mirror:
            items = (
                (socket.offset, socket.diameter, offset),
                (socket.height, socket.small_diameter, offset),
                (
                    extended_cylinder,
                    socket.small_diameter - 4,
                    offset,
                ),
            )
        for height, diameter, dy in items:
            yield "".join(
                (
                    *cylinder_lines,
                    f"translate([{dx:.3f},0,-{dy:.3f}])",
                    f"cylinder(h={height:.3f}, d={diameter:.3f});",
                )
            )

    operations = {
        Socket: generate_socket_lines,
        MultiLevelSocket: generate_multi_level_socket_lines,
    }

    @staticmethod
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
