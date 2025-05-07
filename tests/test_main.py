import pytest

from main import parse_file
from model.socket import Socket, MultiLevelSocket
from model.socket_generator import determine_cylinder_spacing


@pytest.mark.parametrize(
    "length, diameters",
    [
        (2.0, []),
        (42, [2]),
        (2.0, [2, 3]),
    ],
)
def test_determine_spacing_throws_error(length, diameters):
    with pytest.raises(AssertionError):
        determine_cylinder_spacing(length, diameters, 1)


@pytest.mark.parametrize(
    "length, diameters, expected",
    [
        (42.0, [2, 3, 4, 5, 6, 2], 4),
        (42.0, [2, 3, 4], 16.5),
    ],
)
def test_determine_spacing(length, diameters, expected):
    output = determine_cylinder_spacing(length, diameters, 1)
    assert output == expected, "should return the correct spacing values"


def test_parse_file():
    output = list(parse_file("./data/0_5-long-imperial-socket.json"))

    assert output == [
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
