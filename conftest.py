import pytest

from model.configuration import Configuration
from model.socket import Socket
from model.socket_generator import SocketGenerator


@pytest.fixture(scope="session")
def socket_generator():
    return SocketGenerator(
        sockets=[[Socket(height=1, diameter=1, name="test1")]],
        configuration=Configuration(),
    )
