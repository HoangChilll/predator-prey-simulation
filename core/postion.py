class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # =========================
    # SO SÁNH
    # =========================
    def __eq__(self, other):
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))  # để dùng làm key dict/set

    # =========================
    # HIỂN THỊ
    # =========================
    def __repr__(self):
        return f"Position({self.x}, {self.y})"

    # =========================
    # TOÁN HỌC CƠ BẢN
    # =========================
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    # =========================
    # CHUYỂN ĐỔI
    # =========================
    def to_tuple(self):
        return (self.x, self.y)

    @staticmethod
    def from_tuple(t):
        return Position(t[0], t[1])

    # =========================
    # DISTANCE
    # =========================
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    # =========================
    # HÀNG XÓM (4 hướng)
    # =========================
    def neighbors4(self):
        directions = [
            Position(0, 1),
            Position(0, -1),
            Position(1, 0),
            Position(-1, 0)
        ]
        return [self + d for d in directions]