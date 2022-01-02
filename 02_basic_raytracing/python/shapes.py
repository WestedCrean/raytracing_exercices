from PIL import ImageColor
import numpy as np


class Sphere:
    def __init__(self, x=1, y=1, z=1, radius=1, color="red"):
        self.x = x
        self.y = y
        self.z = z
        self.center = np.array((x, y, z))
        self.radius = radius
        self.color = ImageColor.getcolor(color, "RGB")
