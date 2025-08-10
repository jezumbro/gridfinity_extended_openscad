from cqgridfinity import GridfinityDrawerSpacer
from cqkit import INCHES

drawer = GridfinityDrawerSpacer(INCHES(19), INCHES(18.5), verbose=False)

# drawer.render_full_set(False)
drawer.render_half_set()
drawer.save_stl_file("kitchen_drawer.stl", "out")
