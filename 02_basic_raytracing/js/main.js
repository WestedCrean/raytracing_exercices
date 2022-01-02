let Sphere = function(center, radius, color) {
    this.center = center;
    this.radius = radius;
    this.color = color;
}

// Scene setup.
const VIEWPORT_SIZE = 1
const PROJECTION_PLANE_Z = 1
const CAMERA_POSITION = [0, 0, 0]
const BACKGROUND_COLOR = [255, 255, 255]


// Converts 2D canvas coordinates to 3D viewport coordinates.
function canvasToViewport(p2d) {
    return [p2d[0] * VIEWPORT_SIZE / canvas.width,
        p2d[1] * VIEWPORT_SIZE / canvas.height,
        PROJECTION_PLANE_Z]; 
}


// Computes the intersection of a ray and a sphere. Returns the values
// of t for the intersections.
function raySphereIntersection(origin, direction, sphere) {
    let oc = sub(origin, sphere.center)

    let k1 = dot(direction, direction)
    let k2 = 2 * dot(oc, direction)
    let k3 = dot(oc, oc) - sphere.radius * sphere.radius

    let discriminant = k2*k2 - 4*k1*k3
    if (discriminant < 0) {
        return [Infinity, Infinity]
    }

    let t1 = (-k2 + Math.sqrt(discriminant)) / (2 * k1);
    let t2 = (-k2 - Math.sqrt(discriminant)) / (2 * k1);
    return t1, t2
}


// Traces a ray against the set of spheres in the scene.
function tracePixelRay(scene_spheres, origin, direction, min_t, max_t) {
    let closest_t = Infinity;
    let closest_sphere = null;
    
    for (let i = 0; i < scene_spheres.length; i++) {
        let t1, t2 = raySphereIntersection(origin, direction, scene_spheres[i]);
        if (t1 < closest_t && min_t < t1 && t1 < max_t) {
            closest_t = t1;
            closest_sphere = scene_spheres[i];
        }
        if (t2 < closest_t && min_t < t2 && t2 < max_t) {
            closest_t = t2;
            closest_sphere = scene_spheres[i];
        }
    }

    if (closest_sphere == null) {
    return BACKGROUND_COLOR;
    }

    return closest_sphere.color;
}

function init(){
    const canvas = new Canvas()
    const scene_spheres = [
        new Sphere([0, -1, 3], 1, [0, 128, 128]),
        new Sphere([2, 0, 4], 1, [225, 173, 1]),
        new Sphere([-2, 0, 4], 1, [218, 165, 32]),
        new Sphere([-1, 1, 10], 2, [254, 1, 154])
    ]
    const scene_lights = []
    return [ canvas, scene_spheres, scene_lights ]
}

function main() {
    let [ canvas, scene_spheres, scene_lights ] = init()
    console.log({canvas})
    console.log({scene_spheres})
    console.log({"w": canvas.width, "h": canvas.height })
    for (let x = -canvas.width/2; x < canvas.width/2; x++) {
        for (let y = -canvas.height/2; y < canvas.height/2; y++) {
            let direction = canvasToViewport([x, y])
            let color = tracePixelRay(scene_spheres, CAMERA_POSITION, direction, 1, Infinity)
            canvas.putPixel(x, y, color)
        }
    }
    
    canvas.updateCanvas()
}

main()