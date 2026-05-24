WIDTH = 800
HEIGHT = 600
GRID_AREA = int(WIDTH * 0.75)
FPS = 60
def log(msg):
    print(f"[DEBUG] {msg}")
    
def get_cell(size):
    return GRID_AREA // size
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
 
def is_valid(pos, grid):# kiểm tra ô hợp lệ
    x, y = pos
    rows = len(grid)
    cols = len(grid[0])
 
    return (
        0 <= x < rows and
        0 <= y < cols and
        grid[x][y] != 1
    )