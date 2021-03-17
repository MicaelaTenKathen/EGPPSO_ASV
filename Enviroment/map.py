from PIL import Image
import numpy as np


def black_white(resolution, xs, ys):
    im = Image.open(r'C:\Users\mcjara\Downloads\snazzy-image (3).PNG')
    nim = im.resize((xs, ys))
    xn = nim.size[0]
    yn = nim.size[1]
    array = np.zeros((xn, yn))
    img = Image.new('RGB', (xn, yn))
    i = 0
    while i < xn:
        j = 0
        while j < yn:
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
            j += 1
        i += 1
    # img.show()
    # print(array[xi, yi])
    # img.save('map_ypacarai.PNG')
    resolution = resolution
    return array, resolution


def map_values(grid):
    grid_max_x = grid.shape[0]
    grid_max_y = grid.shape[1]

    grid_min = 0

    if grid_max_x < grid_max_y:
        grid_max = grid_max_y
    else:
        grid_max = grid_max_x

    return grid_min, grid_max, grid_max_x, grid_max_y

# df = pd.DataFrame(array)
# df.to_excel('prueba.xlsx', sheet_name='prueba')
# df = pd.read_excel('prueba.xlsx', sheet_name='prueba')
