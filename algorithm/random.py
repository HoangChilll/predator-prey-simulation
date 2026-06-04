
import random
from ui.constants import DIRECTIONS, is_valid
def random_move(grid, self_pos, opponent_pos):
    x, y = self_pos
    moves = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if is_valid((nx, ny), grid):
            moves.append((nx, ny))

    if not moves:
        return self_pos
    return tuple(random.choice(moves))

