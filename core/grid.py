class Grid:
    """
    Grid map:
    0 = đường đi
    1 = tường
    2 = predator
    3 = prey
    """

    EMPTY = 0
    WALL = 1
    PREDATOR = 2
    PREY = 3

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]

    # =========================
    # BASIC
    # =========================
    def in_bounds(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def is_walkable(self, x, y):
        return self.in_bounds(x, y) and self.cells[x][y] != self.WALL

    def is_empty(self, x, y):
        return self.in_bounds(x, y) and self.cells[x][y] == self.EMPTY

    # =========================
    # SET OBJECT
    # =========================
    def set_wall(self, x, y):
        if self.in_bounds(x, y):
            self.cells[x][y] = self.WALL

    def place_predator(self, x, y):
        if self.is_walkable(x, y):
            self.cells[x][y] = self.PREDATOR
            return True
        return False

    def place_prey(self, x, y):
        if self.is_walkable(x, y):
            self.cells[x][y] = self.PREY
            return True
        return False

    # =========================
    # MOVE
    # =========================
    def move(self, x, y, new_x, new_y):
        if not self.is_walkable(new_x, new_y):
            return False

        value = self.cells[x][y]

        if value not in (self.PREDATOR, self.PREY):
            return False  # không có gì để di chuyển

        # xoá vị trí cũ
        self.cells[x][y] = self.EMPTY

        # ghi vị trí mới
        self.cells[new_x][new_y] = value

        return True

    # =========================
    # GET INFO
    # =========================
    def get(self, x, y):
        if self.in_bounds(x, y):
            return self.cells[x][y]
        return None

    # =========================
    # DEBUG / PRINT
    # =========================
    def print_grid(self):
        for row in self.cells:
            print(" ".join(map(str, row)))
        print()

    def load_map(self, map_data):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = map_data[i][j]