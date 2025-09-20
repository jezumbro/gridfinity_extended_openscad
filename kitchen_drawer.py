from pathlib import Path
from cqgridfinity import GridfinityDrawerSpacer
from cqkit import INCHES

directory = Path(__file__).parent / "out" / "kitchen_drawer"


def make_drawer_spacers():
    drawer = GridfinityDrawerSpacer(INCHES(19), INCHES(18.5), verbose=True)

    # drawer.render_full_set(False)
    drawer.render_half_set()
    filename = directory / "kitchen_drawer_spacer.stl"
    drawer.save_stl_file(str(filename.expanduser().absolute()))


if __name__ == "__main__":
    directory.mkdir(parents=True, exist_ok=True)
    make_drawer_spacers()
