
import random
from ui.constants import DIRECTIONS, is_valid
def random_move(grid, self_pos, opponent_pos):
    x, y = self_pos
    print("USING CORRECT RANDOM_MOVE")
    moves = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        print("TRY:", (nx, ny), "VALID:", is_valid((nx, ny), grid))

        if is_valid((nx, ny), grid):
            moves.append((nx, ny))

    if not moves:
        return self_pos
    print("SELF POS:", self_pos, "TYPE:", type(self_pos))
    return tuple(random.choice(moves))

