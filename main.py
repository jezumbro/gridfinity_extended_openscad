from pathlib import Path
from typing import List, Tuple

GRID_WIDTH = 42
SPACING = 1  # mm

NUMBER_OF_ROWS = 2
NUMBER_OF_COLUMNS = 4


def determine_spacing(length: float, cylinders: List[float], min_space=1) -> List[float]:
    """
    Determines the spacing between the sockets based on their diameters.
    The spacing is calculated as the maximum diameter plus a fixed spacing value.
    """
    assert len(cylinders), "The list of diameters cannot be empty."
    num_of_spaces = len(cylinders) + 1
    leftover = length - (sum(cylinders) + min_space * num_of_spaces)
    assert leftover >= 0, "The sum of diameters exceeds the length."
    delta_leftover = (length - sum(cylinders)) / num_of_spaces
    return [delta_leftover] * num_of_spaces


def generate_block(socket_array: List[Tuple[float]]):
    """
    Generates a block of code for each socket in the socket array."""


if __name__ == "__main__":
    # Get the current working directory
    current_directory = Path.cwd()

    # Print the current working directory
    print(f"Current working directory: {current_directory}")

    # Create a new directory named 'new_directory'
    new_directory = current_directory / "new_directory"
    new_directory.mkdir(exist_ok=True)

    # Print the new directory path
    print(f"New directory created: {new_directory}")
