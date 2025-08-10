import pytest

from model.socket import MultiLevelSocket, Socket


@pytest.mark.parametrize(
    "length, diameters",
    [
        (2.0, []),
        (42, [2]),
        (2.0, [2, 3]),
    ],
)
def test_determine_spacing_throws_error(socket_generator, length, diameters):
    with pytest.raises(AssertionError):
        socket_generator.determine_cylinder_spacing(length, diameters, 1)


@pytest.mark.parametrize(
    "length, diameters, expected",
    [
        (42.0, [2, 3, 4, 5, 6, 2], 4),
        (42.0, [2, 3, 4], 16.5),
    ],
)
def test_determine_spacing(socket_generator, length, diameters, expected):
    output = socket_generator.determine_cylinder_spacing(length, diameters, 1)
    assert output == expected, "should return the correct spacing values"
