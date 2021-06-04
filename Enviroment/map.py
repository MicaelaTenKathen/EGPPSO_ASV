from PIL import Image
import numpy as np


def black_white(resolution, xs, ys):
    im = Image.open(r'C:\Users\mcjara\OneDrive - Universidad Loyola '
                    r'Andalucía\Documentos\PycharmProjects\EGPPSO_ASV\Image\snazzy-image-prueba.png')
    nim = im.resize((xs, ys))
    array = np.zeros((xs, ys))
    img = Image.new('RGB', (xs, ys))
    j = 0

    while j < ys:
        i = 0
        while i < xs:
            r, g, b = nim.getpixel((i, j))
            p = (r * 0.3 + g * 0.59 + b * 0.11)
            gray = int(p)
            if gray < 225:
                color = 255
                bit = 0
            else:
                color = 0
                bit = 1
            pixel = tuple([color, color, color])
            img.putpixel((i, j), pixel)
            array[i, j] = int(bit)
            i += 1
        j += 1
    resolution = resolution
    return array, resolution


def map_values(xs, ys):
    grid_max_x = xs
    grid_max_y = ys

    grid_min = 0

    if grid_max_x < grid_max_y:
        grid_max = grid_max_y
    else:
        grid_max = grid_max_x

    return grid_min, grid_max, grid_max_x, grid_max_y
