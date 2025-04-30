import pytest
from main import determine_cylinder_spacing, write_translations, Socket


@pytest.mark.parametrize(
    "length, diameters",
    [
        (2.0, []),
        (2.0, [2, 3]),
    ],
)
def test_determine_spacing_throws_error(length, diameters):
    with pytest.raises(AssertionError):
        determine_cylinder_spacing(length, diameters)


@pytest.mark.parametrize(
    "length, diameters, expected",
    [
        (42.0, [2], 20),
        (42.0, [2, 3, 4, 5, 6, 1], 3),
        (42.0, [2, 3, 4], 8.25),
    ],
)
def test_determine_spacing(length, diameters, expected):
    output = determine_cylinder_spacing(length, diameters)
    assert output == expected, "should return the correct spacing values"
