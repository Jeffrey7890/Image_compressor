from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

from Quadtree import XY, AABB
from visualize2_0 import draw
import math



class CompressionTree:
    THRESHOLD = 10
    MAX_DEPTH = 6

    def __init__(self, pixels, current_depth, boundary: AABB):
        self._boundary = boundary
        self.pixels = pixels
        self.current_depth = current_depth
        self._colors = np.array([0, 0, 0], dtype=np.float32)

        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def insert(self):
        is_uniform, avg_color = self.uniform_region(self._boundary)

        if is_uniform or self.current_depth == self.MAX_DEPTH:
            self._colors = avg_color
            return

        # Subdivide if not uniform
        if self.northWest is None:
            self.subdivide()

        # Insert into children
        self.northWest.insert()
        self.northEast.insert()
        self.southWest.insert()
        self.southEast.insert()

    def subdivide(self):
        x, y = self._boundary._cnt.x, self._boundary._cnt.y
        half = self._boundary._hlfDim / 2

        # Define four quadrants
        nw = AABB(XY(x - half, y - half), half)
        ne = AABB(XY(x + half, y - half), half)
        sw = AABB(XY(x - half, y + half), half)
        se = AABB(XY(x + half, y + half), half)

        self.northWest = CompressionTree(self.pixels, self.current_depth + 1, nw)
        self.northEast = CompressionTree(self.pixels, self.current_depth + 1, ne)
        self.southWest = CompressionTree(self.pixels, self.current_depth + 1, sw)
        self.southEast = CompressionTree(self.pixels, self.current_depth + 1, se)

    def uniform_region(self, boundary: AABB):
        """Check if region is uniform using std deviation."""
        x, y, h = boundary._cnt.x, boundary._cnt.y, boundary._hlfDim

        x0 = int(max(x - h, 0))
        y0 = int(max(y - h, 0))
        x1 = int(min(x + h, self.pixels.shape[1]))
        y1 = int(min(y + h, self.pixels.shape[0]))

        region = self.pixels[y0:y1, x0:x1]
        if region.size == 0:
            return True, np.array([0, 0, 0])

        avg_color = np.mean(region, axis=(0, 1))
        std = np.std(region)
        return std < self.THRESHOLD, avg_color


class PltRect:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    def __len__(self):
        return len(self.color)


def render_quadtree(node, cmp_image):
    """Recursively collect rectangles."""
    if node.northWest is not None:
        render_quadtree(node.northWest, cmp_image)
        render_quadtree(node.northEast, cmp_image)
        render_quadtree(node.southWest, cmp_image)
        render_quadtree(node.southEast, cmp_image)

    x, y, h = node._boundary.value()
    rect_size = h * 2
    if node._colors[0] > 0 or node._colors[1] > 0 or node._colors[2] > 0:
        color = node._colors
        cmp_image.append(PltRect(x - h, y - h, rect_size, (float(color[0]), float(color[1]), float(color[2]))))


def get_pixels(file_name, fmt='RGB', resize=None):
    img = Image.open(file_name).convert(fmt)
    if resize is not None:
        w, h = img.size
        print(w, h)
        img = img.resize((w//resize, h//resize), Image.LANCZOS)
    pixels = np.array(img)

    return pixels



def save_image(cmp_image):
    n = len(cmp_image)
    width = int(math.sqrt(n))
    height = math.ceil(n /width)
    pixels = [p.color for p in cmp_image]
    print(len(pixels), " pixels")
    print(pixels[:3])
    pixels += [(0, 0, 0)] * (width*height-n)
    img_array = np.array(pixels, dtype=np.uint8).reshape((height, width, 3))
    img = Image.fromarray(img_array)
    img.save("output.png")


def main(**kwargs):
    file_name = kwargs.get('file_name')
    threshold = kwargs.get('threshold')
    max_depth = kwargs.get('max_depth')
    d = kwargs.get('d')
    r = kwargs.get('r')

    if file_name is None:
        print("Usage: image_compress [file_name]")
        return
    pixels = get_pixels(file_name, fmt='RGB', resize=2)
    w, h = pixels.shape[:2]
    print(pixels[0].shape)
    cnt = XY(w / 2, h / 2)
    boundary = AABB(cnt, max(w, h) / 2)

    if threshold is not None:
        CompressionTree.THRESHOLD = threshold
    if max_depth is not None:
        CompressionTree.MAX_DEPTH = max_depth

    print('\nSize before compression = ', w*h,
        '\nThreshold:', CompressionTree.THRESHOLD, 
        'max depth:', CompressionTree.MAX_DEPTH)
    tree = CompressionTree(pixels, 0, boundary)
    tree.insert()
    cmp_image = []
    render_quadtree(tree, cmp_image)
    print(cmp_image[0].color)
    print('\nSize after compression = ',len(cmp_image))
    if d is None:
        return
    # save_image(cmp_image)
    draw(w, h, cmp_image)


if __name__ == "__main__":

    main(file_name='fresh_pepper.jpeg', threshold=5, max_depth=6, d='d')