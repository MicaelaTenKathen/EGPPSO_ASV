import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd

def black_white():
    im = Image.open(r'C:\Users\mcjara\Downloads\snazzy-image (3).PNG')
    xs = 1000
    ys = 1500
    xi = 0
    yi = 0
    # Resize the image
    nim = im.resize((xs,ys))
    # Image dimensions
    xn = nim.size[0]
    yn = nim.size[1]
    array = np.zeros((xn, yn))
    # New image
    img = Image.new('RGB', (xn, yn))
    i = 0
    while i < xn:
        j = 0
        while j < yn:
            # Pixel RGB
            r, g, b = nim.getpixel((i,j))
            # Grayscale equivalent
            p = (r * 0.3 + g * 0.59 + b * 0.11)
            # Integer value
            gray = int(p)
            if gray < 225:
                color = 255
                bit = 0
            else:
                color = 0
                bit = 1
            pixel = tuple([color, color, color])
            # New color
            img.putpixel((i,j), pixel)
            array[i, j] = int(bit)
            j += 1
        i += 1
    # img.show()
    #print(array[xi, yi])
    img.save('map_ypacarai.PNG')
    return array

grid = black_white()

# df = pd.DataFrame(array)
# df.to_excel('prueba.xlsx', sheet_name='prueba')
# df = pd.read_excel('prueba.xlsx', sheet_name='prueba')
