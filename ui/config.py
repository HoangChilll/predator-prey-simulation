def to_pixel(pos, cell):
    row, col = pos
    return col * cell, row * cell


def in_grid(pos, size):
    r, c = pos
    return 0 <= r < size and 0 <= c < size