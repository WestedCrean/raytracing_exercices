import matplotlib.pyplot as plt
import numpy as np
from shapes import Sphere
from lights import PositionalLight

IMAGE_WIDTH = 100  # 1920
IMAGE_HEIGHT = 100  # 1080
IMAGE_RATIO = float(IMAGE_WIDTH) / IMAGE_HEIGHT

BACKGROUND_COLOR = np.zeros((255, 255, 255))


def initialize():
    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3))

    screen = (-1, 1 / IMAGE_RATIO, 1, -1 / IMAGE_RATIO)
    camera = np.array([0, 0, 1])

    scene = [
        Sphere(-0.2, 0, -1, radius=0.7, diffuse=np.array([218, 255, 63])),
        Sphere(0.1, -0.3, 0, radius=0.1, diffuse=np.array([0, 255, 205])),
        Sphere(-0.3, 0, 0, radius=0.15, diffuse=np.array([27, 44, 193])),
    ]

    light = PositionalLight(5.0, 5.0, 5.0)
    return image, screen, camera, scene, light


def ray_sphere_intersection(origin, direction, sphere):
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
    return vector / 255


def nearest_intersected_object(objects, ray_origin, ray_direction):
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


def raytrace(image, screen, camera, scene, light):
    # main code goes here
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
            intersection_to_light = normalize(light.position - shifted_point)

            _, min_distance = nearest_intersected_object(scene, origin, direction)
            intersection_to_light_distance = np.linalg.norm(
                light.position - intersection
            )
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                continue

            illumination = np.zeros((3))

            # ambient
            illumination += nearest_object.ambient * light.ambient

            # diffuse
            illumination += (
                nearest_object.diffuse
                * light.diffuse
                * np.dot(intersection_to_light, normal_to_surface)
            )

            # specular
            intersection_to_camera = normalize(camera - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += (
                nearest_object.specular
                * light.specular
                * np.dot(normal_to_surface, H) ** (nearest_object.shininess / 4)
            )

            image[i, j] = normalize_color(illumination)
            # print("%d/%d" % (i + 1, height))
    return image


def save(image, img_name="test_image.png"):
    # im.save(img_name)
    plt.imsave(img_name, image)


def main():
    image, screen, camera, scene, light = initialize()
    image = raytrace(image, screen, camera, scene, light)
    save(image)


if __name__ == "__main__":
    main()
