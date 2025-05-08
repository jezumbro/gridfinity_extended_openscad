import json
from pathlib import Path
from typing import Iterable, List

from loguru import logger
from pydantic import BaseModel, Field
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


class Configuration(BaseModel):
    tolerance: float = 0.25


class DataModel(BaseModel):
    sockets: List[List[MultiLevelSocket | Socket]]
    configuration: Configuration = Field(default_factory=Configuration)


if __name__ == "__main__":
    filename: str = "data/0_25-small-set.json"
    data = DataModel.model_validate_json(open(filename, "r").read())
    socket_generator = SocketGenerator(
        sockets=data.sockets,
        tolerance=data.configuration.tolerance,
        stackable=True,
        rows=2,
    )
    socket_generator.write_file(Path("main.scad"))
