import numpy as np
from numba import int32, float64
from numba.experimental import jitclass

spec = [
    ("center", float64[:]),
    ("radius", float64),
    ("shininess", int32),
    ("diffuse", float64[:]),
    ("ambient", float64[:]),
    ("specular", float64[:]),
]


@jitclass(spec)
class Sphere:
    def __init__(
        self,
        center=np.array([0.0, 0.0, 0.0]),
        radius=1.0,
        diffuse=np.array([1.0, 1.0, 1.0]),
        shininess=100,
        ambient=np.array([0.0, 0.0, 0.0]),
        specular=np.array([1.0, 1.0, 1.0]),
    ):
        self.radius = radius
        self.center = center

        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
