class Canvas{
    constructor() {
        this.canvas = document.getElementById("canvas");
        this.width = this.canvas.width
        this.height = this.canvas.height
        this.canvas_context = this.canvas.getContext("2d");
        this.canvas_buffer = this.canvas_context.getImageData(0, 0, this.canvas.width, this.canvas.height);
        this.canvas_pitch = this.canvas_buffer.width * 4;
      }

    putPixel(x, y, color) {
        x = this.canvas.width/2 + x;
        y = this.canvas.height/2 - y - 1;
    
        if (x < 0 || x >= this.canvas.width || y < 0 || y >= this.canvas.height) {
        return;
        }
    
        let offset = 4*x + this.canvas_pitch*y;
        this.canvas_buffer.data[offset++] = color[0];
        this.canvas_buffer.data[offset++] = color[1];
        this.canvas_buffer.data[offset++] = color[2];
        this.canvas_buffer.data[offset++] = 255; // Alpha = 255 (full opacity)
    }
    
    
    // Displays the contents of the offscreen buffer into the canvas.
    updateCanvas() {
        this.canvas_context.putImageData(this.canvas_buffer, 0, 0);
    }
}

/**
 * Linear algebra
 */

// Dot product of two 3D vectors.
function dot(v1, v2) {
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2];  
}

// Computes v1 - v2.
function sub(v1, v2) {
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]];
}