import numpy as np


class Sphere:
    def __init__(
        self,
        x=1,
        y=1,
        z=1,
        radius=1,
        ambient=np.array([0, 0, 0]),
        diffuse=np.array([1, 1, 1]),
        specular=np.array([1, 1, 1]),
        shininess=100,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.center = np.array([x, y, z])

        self.ambient = ambient
        self.diffuse = diffuse
        self.color = diffuse
        self.specular = specular
        self.shininess = shininess
