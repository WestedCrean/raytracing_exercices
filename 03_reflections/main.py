from random import choice
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import numba
from numba import jit, float64, optional
from shapes import Sphere
from lights import PositionalLight
from halo import Halo

IMAGE_WIDTH = 200  # 1920
IMAGE_HEIGHT = 200  # 1080
IMAGE_RATIO = float(IMAGE_WIDTH) / IMAGE_HEIGHT

BACKGROUND_COLOR = np.zeros((255, 255, 255))


def initialize():
    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3))

    screen = (-1, 1 / IMAGE_RATIO, 1, -1 / IMAGE_RATIO)
    camera = np.array([0, 0, 1])

    scene = [
        Sphere(
            np.array([-0.2, 0.0, -1.0]),
            0.7,
            np.array([218.0, 255.0, 63.0]),
            70,
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
        ),
        Sphere(
            np.array([0.1, -0.3, 0.0]),
            0.1,
            np.array([0.0, 255.0, 205.0]),
            100,
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
        ),
        Sphere(
            np.array([-0.3, 0.0, 0.0]),
            0.15,
            np.array([27.0, 44.0, 193.0]),
            100,
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
        ),
        Sphere(
            np.array([0.5, 1.0, 0.0]),
            0.05,
            np.array([189.0, 44.0, 193.0]),
            20,
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
        ),
    ]

    # random spheres

    for _ in range(0, 6):
        scene.append(
            Sphere(
                np.array(
                    [
                        (np.random.poisson(2, 1) * np.random.normal(0, 1, 1))[0],
                        (np.random.poisson(2, 1) * np.random.normal(0, 1, 1))[0],
                        (np.random.poisson(2, 1) * np.random.normal(0, 1, 1))[0],
                    ]
                ),
                0.2,
                np.array(
                    [
                        np.random.normal(255 // 2, 255 // 2),
                        np.random.normal(255 // 2, 255 // 2),
                        np.random.normal(255 // 2, 255 // 2),
                    ]
                ),
                100,
                np.array([0.0, 0.0, 0.0]),
                np.array([1.0, 1.0, 1.0]),
            )
        )

    lights = [
        PositionalLight(
            np.array([5.0, 5.0, 5.0]),
            np.array(
                [
                    1.0,
                    1.0,
                    1.0,
                ]
            ),
            np.array(
                [
                    1.0,
                    1.0,
                    1.0,
                ]
            ),
            np.array(
                [
                    1.0,
                    1.0,
                    1.0,
                ]
            ),
        ),
        # PositionalLight(-5.0, -5.0, 5.0),
    ]
    return image, screen, camera, scene, lights


def ray_sphere_intersection(origin, direction, sphere: Sphere) -> optional(float64):
    b = 2 * np.dot(direction, origin - sphere.center)
    c = np.linalg.norm(origin - sphere.center) ** 2 - sphere.radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def normalize(vector):
    return vector / np.linalg.norm(vector)


def normalize_color(vector):
    return np.clip(vector / 255, 0, 1)


def nearest_intersected_object(
    objects: List[Sphere], ray_origin, ray_direction
) -> numba.types.Tuple((optional(Sphere), float64)):
    distances = [
        ray_sphere_intersection(ray_origin, ray_direction, obj) for obj in objects
    ]
    nearest_object = None
    min_distance = np.inf

    index = 0
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance


def compute_lighting(
    lights,
    scene,
    shifted_point,
    normal_to_surface,
    nearest_object,
    intersection_to_camera,
    intersection,
):

    illumination = np.zeros((3))

    for light in lights:

        intersection_to_light = normalize(light.position - shifted_point)

        _, min_distance = nearest_intersected_object(
            scene, shifted_point, intersection_to_light
        )
        intersection_to_light_distance = np.linalg.norm(light.position - intersection)
        is_shadowed = min_distance < intersection_to_light_distance

        if is_shadowed:
            continue

        # ambient
        illumination += nearest_object.ambient * light.ambient

        # diffuse
        illumination += (
            nearest_object.diffuse
            * light.diffuse
            * np.dot(intersection_to_light, normal_to_surface)
        )

        # specular
        H = normalize(intersection_to_light + intersection_to_camera)
        illumination += (
            nearest_object.specular
            * light.specular
            * np.dot(normal_to_surface, H) ** (nearest_object.shininess / 4)
        )

    return illumination


def raytrace(image, screen, camera, scene, lights):
    # main code goes here

    spinner = Halo(text=f"Progress: {0:.2f}%", spinner="dots")
    spinner.start()

    for i, y in enumerate(np.linspace(screen[1], screen[3], IMAGE_HEIGHT)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], IMAGE_WIDTH)):

            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)

            # check for intersections
            nearest_object, min_distance = nearest_intersected_object(
                scene, origin, direction
            )

            if not nearest_object:
                continue

            intersection = origin + min_distance * direction

            normal_to_surface = normalize(intersection - nearest_object.center)
            shifted_point = intersection + 1e-5 * normal_to_surface

            intersection_to_camera = normalize(camera - intersection)
            illumination = compute_lighting(
                lights,
                scene,
                shifted_point,
                normal_to_surface,
                nearest_object,
                intersection_to_camera,
                intersection,
            )

            image[i, j] = normalize_color(illumination)

        spinner.text = f"Progress: {i/IMAGE_HEIGHT*100:.2f}%"

    spinner.stop()
    return image


def save(image, img_name="test_image.png"):
    saved = False
    while not saved:
        try:
            plt.imsave(img_name, image)
            saved = True
        except Exception as e:
            print(e)
            import random

            chars = ["abcdefghijklmnopqrstuvwxyz1234567890"]
            img_name = "" + random.choice(chars) + img_name


def main():
    image, screen, camera, scene, light = initialize()
    image = raytrace(image, screen, camera, scene, light)
    save(image)


if __name__ == "__main__":
    main()
