import numpy as np


class PositionalLight:
    def __init__(
        self,
        x=1.0,
        y=1.0,
        z=1.0,
        ambient=np.array(
            [
                1,
                1,
                1,
            ]
        ),
        diffuse=np.array(
            [
                1,
                1,
                1,
            ]
        ),
        specular=np.array(
            [
                1,
                1,
                1,
            ]
        ),
    ):
        self.position = np.array((x, y, z))
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
