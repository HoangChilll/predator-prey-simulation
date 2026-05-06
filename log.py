
from ui.map import GRID_AREA

def log(msg):
    print(f"[DEBUG] {msg}")
    
def get_cell(size):
    return GRID_AREA // size