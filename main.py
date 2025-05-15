import os
import subprocess
from pathlib import Path
from typing import List

from loguru import logger
from pydantic import BaseModel, Field

from model.socket import MultiLevelSocket, Socket
from model.socket_generator import SocketGenerator
from model.configuration import Configuration

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


class DataModel(BaseModel):
    sockets: List[List[MultiLevelSocket | Socket]]
    configuration: Configuration = Field(default_factory=Configuration)


if __name__ == "__main__":
    input_file: Path = Path("data") / "0_5-long-metric.json"
    data = DataModel.model_validate_json(open(input_file.absolute(), "r").read())
    socket_generator = SocketGenerator(
        sockets=data.sockets,
        configuration=data.configuration,
    )
    temp_file = Path("main.scad")
    socket_generator.write_file(temp_file)
    output_filename = Path("out") / input_file.name.replace(".json", ".stl")
    try:
        subprocess.run(
            [
                "openscad",
                "-o",
                f"{output_filename.relative_to('.')}",
                "--export-format",
                "binstl",
                temp_file,
            ]
        )
    except subprocess.TimeoutExpired:
        logger.error("Command timed out")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}", e.stderr)
