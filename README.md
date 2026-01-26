# Quadtree Image Compression

This project implements a **Quadtree-based image compression system** in Python. The goal is to explore how spatial data structures can be applied to compress images while preserving important visual details.

Quadtrees recursively divide a 2D space into four quadrants, subdividing regions with more detail and leaving uniform areas larger. This approach reduces data storage while maintaining perceptually important information.

---

## Features

* **Quadtree Implementation:** Recursively partitions an image into regions based on color uniformity.
* **Adaptive Compression:** Regions with little variation are stored as a single color; regions with more detail are subdivided further.
* **Customizable Parameters:**

  * `THRESHOLD`: Maximum standard deviation allowed for a region to be considered uniform.
  * `MAX_DEPTH`: Maximum recursion depth of the quadtree.
* **Visualization:** Uses `matplotlib` to draw the compressed representation.
* **Image Processing:** Supports resizing and RGB color format.

---

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd quadtree-image-compression
```

2. Install required Python packages:

```bash
pip install Pillow matplotlib numpy
```

3. Ensure the following modules are present in your project:

* `Quadtree.py` (contains `XY` and `AABB` classes)
* `visualize2_0.py` (contains `draw` function)

---

## Usage

```python
python main.py
```

Or call the main function with parameters:

```python
main(
    file_name='fresh_pepper.jpeg',  # input image file
    threshold=5,                     # optional: max std deviation
    max_depth=6,                     # optional: maximum quadtree depth
    d='d'                            # optional: enables drawing
)
```

### Parameters:

* `file_name`: Path to the input image file.
* `threshold` (optional): Determines the sensitivity to color variation. Lower values preserve more detail.
* `max_depth` (optional): Controls the maximum quadtree depth.
* `d` (optional): If specified, displays the quadtree visualization.

---

## How It Works

1. **Load Image:** The image is converted to RGB and optionally resized.
2. **Quadtree Construction:** A `CompressionTree` object recursively subdivides the image into quadrants:

   * Each node checks if the region is uniform (based on standard deviation of colors).
   * Uniform regions store the average color.
   * Non-uniform regions are subdivided up to `MAX_DEPTH`.
3. **Render:** The quadtree is rendered into rectangles representing compressed color blocks.
4. **Visualization:** The `draw` function displays the compressed image as a grid of colored rectangles.
5. *(Optional)* **Save Image:** The compressed image can be saved using `save_image()`.

---

## Example

```python
main(file_name='fresh_pepper.jpeg', threshold=5, max_depth=6, d='d')
```

This will compress the image using a quadtree and display the resulting colored rectangles.

---

## Key Learnings

* How recursion and spatial data structures can be applied in image compression.
* Trade-offs between compression ratio and image detail.
* Techniques for visualizing quadtree-based image representations.

---

## Dependencies

* Python 3.8+
* [Pillow](https://pypi.org/project/Pillow/)
* [NumPy](https://pypi.org/project/numpy/)
* [Matplotlib](https://pypi.org/project/matplotlib/)

---

## License

This project is for **educational purposes**. You are free to explore, modify, and learn from it.
