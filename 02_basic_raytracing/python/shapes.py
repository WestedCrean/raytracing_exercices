from PIL import ImageColor
import numpy as np
from numba import int32, float32
from numba.typed import string
from numba.experimental import jitclass

spec = [
    ("x", float32),
    ("y", float32),
    ("z", float32),
    ("radius", float32),
    ("center", float32[:]),  # an array field
    ("color", string),
]


@jitclass(spec)
class Sphere:
    def __init__(self, x=1, y=1, z=1, radius=1, color="red"):
        self.x = x
        self.y = y
        self.z = z
        self.center = np.array((x, y, z))
        self.radius = radius
        self.color = ImageColor.getcolor(color, "RGB")
