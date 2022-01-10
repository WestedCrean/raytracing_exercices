import numpy as np
from numba import int32, float64
from numba.experimental import jitclass

spec = [
    ("position", float64[:]),
    ("ambient", float64[:]),
    ("diffuse", float64[:]),
    ("specular", float64[:]),
    ("shininess", int32),
]


@jitclass(spec)
class PositionalLight:
    def __init__(
        self,
        position=np.array([1.0, 1.0, 1.0]),
        ambient=np.array(
            [
                1.0,
                1.0,
                1.0,
            ]
        ),
        diffuse=np.array(
            [
                1.0,
                1.0,
                1.0,
            ]
        ),
        specular=np.array(
            [
                1.0,
                1.0,
                1.0,
            ]
        ),
    ):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
