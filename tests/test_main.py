import pytest

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
