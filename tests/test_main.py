import pytest
from main import determine_spacing


@pytest.mark.parametrize(
    "length, diameters",
    [
        (2.0, []),
        (2.0, [2, 3]),
    ],
)
def test_determine_spacing_throws_error(length, diameters):
    with pytest.raises(AssertionError):
        determine_spacing(length, diameters)


@pytest.mark.parametrize(
    "length, diameters, expected",
    [
        (42.0, [2], [20, 20]),
        (42.0, [2, 3, 4, 5, 6, 1], [3] * 7),
        (42.0, [2, 3, 4], [8.25, 8.25, 8.25, 8.25]),
    ],
)
def test_determine_spacing(length, diameters, expected):
    output = determine_spacing(length, diameters)
    assert (
        len(output) == len(diameters) + 1
    ), "should have 1 more than the length diameter"
    assert output == expected, "should return the correct spacing values"


def test_assert_hi():
    assert True, "should have setup pytest correctly to run this test"
