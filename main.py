from pathlib import Path

from model.socket import MultiLevelSocket, Socket
from model.socket_generator import SocketGenerator

metric_test_set = [
    Socket(height=28.5, diameter=18.35, name="13mm"),
    Socket(height=28.5, diameter=20.35, name="14mm"),
    Socket(height=28.5, diameter=22.25, name="15mm"),
]
imperial_test_set = [
    MultiLevelSocket(
        height=28.5,
        diameter=17.5,
        name="1/4",
        small_diameter=10.5,
        transition_length=3,
        offset=14,
    ),
    MultiLevelSocket(
        height=28.5,
        diameter=17.5,
        name="5/16",
        small_diameter=12.5,
        transition_length=3,
        offset=14.5,
    ),
    MultiLevelSocket(
        height=28.5,
        diameter=17.5,
        name="3/8",
        small_diameter=14.9,
        transition_length=3,
        offset=14.75,
    ),
    MultiLevelSocket(
        height=28.5,
        diameter=17.5,
        name="7/16",
        small_diameter=16.5,
        transition_length=3,
        offset=15,
    ),
]
main_set = [
    MultiLevelSocket(
        height=64,
        diameter=17.5,
        name="7/16",
        small_diameter=16.75,
        transition_length=3,
        offset=39,
    ),
    Socket(height=64, diameter=18.4, name="1/2"),
    Socket(height=64, diameter=20.1, name="9/16"),
    Socket(height=64, diameter=22.25, name="5/8"),
    Socket(height=64, diameter=24.3, name="11/16"),
    Socket(height=64, diameter=26.1, name="3/4"),
]
if __name__ == "__main__":
    socket_generator = SocketGenerator(sockets=main_set, stackable=True)
    socket_generator.write_file(Path("main.scad"))
