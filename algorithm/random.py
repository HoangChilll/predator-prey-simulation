
import random
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

DIRECTIONS = [
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
    (-1, 0)   # up
]
def is_valid(pos, grid):
    x, y = pos
    n = len(grid)
    print("GRID SIZE:", len(grid))
    return 0 <= x < n and 0 <= y < n 