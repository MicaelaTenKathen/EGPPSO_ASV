

def ratio_s(x_int, y_int, grid, part):
    x_int = int(x_int)
    y_int = int(y_int)
    x_left = x_int + 2
    x_right = x_int - 2
    y_up = y_int + 2
    y_down = y_int - 2
    x_i = int(part[0])
    y_i = int(part[1])
    if grid[x_right, y_down] == 1:
        part[0] = x_right
        part[1] = y_down
    else:
        if grid[x_int, y_down] == 1:
            part[1] = y_down
            part[0] = x_int
        else:
            if grid[x_left, y_i] == 1:
                part[0] = x_left
                part[1] = y_int
            else:
                if grid[x_right, y_i] == 1:
                    part[0] = x_right
                    part[1] = y_int
                else:
                    if grid[x_i, y_up] == 1:
                        part[1] = y_up
                        part[0] = x_int
                    else:
                        part[0] = x_i
                        part[1] = y_i
    return part