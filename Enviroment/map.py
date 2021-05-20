from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def black_white(resolution, xs, ys):
    im = Image.open(r'C:\Users\mcjara\OneDrive - Universidad Loyola Andalucía\Documentos\PycharmProjects\PSO_ASVs\Image'
                    r'\snazzy-image-prueba.png')
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
    # img.show()
    # print(array[xi, yi])
    # img.save('map_ypacarai.PNG')
    resolution = resolution
    return array, resolution


# grid, res = black_white(1, 100, 150)
# grid[grid == 0] = np.nan
# img.show()
# img.save("Ypacarai_lake.png")
# new_grid = pd.DataFrame.to_numpy(new_grid)


#

# minz = np.min(_z)
#
# im4 = plt.imshow(grid.T)  # for imshow the array must be transposed
# plt.colorbar(im4, format='%.2f', shrink=1)
# plt.xlabel("x [m]")
# plt.ylabel("y [m]")
# plt.ylim([0, 1500])
# # Axs[1].set_aspect('equal')
# # plt.title('Ground Truth')
# plt.grid(True)
# # plt.savefig("map.PNG")
plt.show()

def map_values(xs, ys):
    grid_max_x = xs
    grid_max_y = ys

    grid_min = 0

    if grid_max_x < grid_max_y:
        grid_max = grid_max_y
    else:
        grid_max = grid_max_x

    return grid_min, grid_max, grid_max_x, grid_max_y

# df = pd.DataFrame(array)
# df.to_excel('prueba.xlsx', sheet_name='prueba')
# df = pd.read_excel('prueba.xlsx', sheet_name='prueba')
