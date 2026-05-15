WIDTH = 800
HEIGHT = 600
GRID_AREA = int(WIDTH * 0.75)
FPS = 60
def log(msg):
    print(f"[DEBUG] {msg}")
    
def get_cell(size):
    return GRID_AREA // size