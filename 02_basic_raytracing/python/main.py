from PIL import Image, ImageColor
import numpy as np
from shapes import Sphere

IMAGE_WIDTH = 600  # 1920
IMAGE_HEIGHT = 600  # 1080

VIEWPORT_SIZE = 1

CAMERA_TO_VIEWPORT = 1  # d

BACKGROUND_COLOR = ImageColor.getcolor("black", "RGB")

scene_spheres = [
    Sphere(0, 1, 3, radius=1, color="purple"),
    Sphere(2, 0, 4, radius=1, color="yellow"),
    Sphere(3, 1, 4, radius=1, color="red"),
]


def initialize():
    im = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
    return im


def ray_sphere_intersection(origin, direction, sphere: Sphere):
    r = sphere.radius
    CO = origin - sphere.center

    a = np.dot(direction, direction)
    b = 2 * np.dot(CO, direction)
    c = np.dot(CO, CO) - r * r

    # print(f"direction: {direction}")
    # print(f"a,b,c = {a} {b} {c}")

    discriminant = (b * b) - 4 * (a * c)

    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b + np.sqrt(discriminant)) / (2 * a)

    return t1, t2


def trace_pixel_ray(origin, direction, t_min, t_max):
    # the ray equation
    # P = O + t(V-O)
    # or using vector D = (V - O) as direction of ray
    # P = O + tD

    closest_t = np.inf  # infinity
    closest_sphere = None

    for sphere in scene_spheres:
        t1, t2 = ray_sphere_intersection(origin, direction, sphere)

        if t_min <= t1 <= t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t_min <= t2 <= t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if not closest_sphere:
        return BACKGROUND_COLOR

    return closest_sphere.color


def canvas_to_viewport(x, y):
    return (
        x * (VIEWPORT_SIZE / IMAGE_WIDTH),
        y * (VIEWPORT_SIZE / IMAGE_HEIGHT),
        CAMERA_TO_VIEWPORT,
    )


def raytrace(im: Image):
    # main code goes here

    # 1. place the camera and the viewport as desired
    camera_origin = np.array((0, 0, 0))

    # for pixel on canvas:
    # for x in range(-IMAGE_WIDTH // 2, IMAGE_WIDTH // 2):
    # for y in range(-IMAGE_HEIGHT // 2, IMAGE_HEIGHT // 2):
    for x in range(im.width):
        for y in range(im.height):
            # 2. determine which square on viewport corresponds to this pixel
            D = canvas_to_viewport(x, y)

            # 3. determine the color seen through that square
            color = trace_pixel_ray(camera_origin, D, 1, 1000)

            # 4. paint the pixel with that color
            im.putpixel((x, y), color)

    return im


def save(im, img_name="test_image.png"):
    im.save(img_name)


def main():
    im = initialize()
    im = raytrace(im)
    save(im)


if __name__ == "__main__":
    main()