import json
from pathlib import Path

from loguru import logger
from pydantic_core import ValidationError

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


def parse_file(filename: str):
    data = json.load(open(filename, "r"))
    for row in data:
        try:
            yield MultiLevelSocket.model_validate(row)
            continue
        except ValidationError as e:
            ...
        try:
            yield Socket.model_validate(row, by_alias=True)
        except ValidationError as e:
            logger.error(e)


if __name__ == "__main__":
    socket_generator = SocketGenerator(
        sockets=list(parse_file("./data/0_25-long-imperial.json")),
        tolerance=0.25,
        stackable=True,
    )
    socket_generator.write_file(Path("main.scad"))
