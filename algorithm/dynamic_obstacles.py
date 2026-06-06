import random


class DynamicObstacleManager:
    """
    Quản lý lớp vật cản động (dynamic obstacle layer) độc lập với bản đồ gốc.

    - static_grid : ma trận gốc (không bị thay đổi)
    - seed        : seed cố định để đảm bảo reproducibility
    - update_interval: cứ sau bao nhiêu bước thì cập nhật vật cản
    """

    OBSTACLE_VALUE = 2  # giá trị đánh dấu ô vật cản động trong effective grid

    def __init__(self, static_grid, seed: int = 42, update_interval: int = 3):
        self.static_grid = static_grid
        self.seed = seed
        self.update_interval = update_interval

        rows = len(static_grid)
        cols = len(static_grid[0]) if rows > 0 else 0
        free_count = sum(
            1 for r in range(rows) for c in range(cols)
            if static_grid[r][c] == 0
        )
        self.max_obstacles = max(3, min(10, free_count // 15))

        self._rng = random.Random(seed)
        self.obstacles: set[tuple[int, int]] = set()
        self._dirty = True
        self._cached_grid: list[list[int]] | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(self, step: int, predator_pos: tuple, prey_pos: tuple) -> None:
        """Gọi sau mỗi bước sim. Chỉ thực sự cập nhật khi đến interval."""
        if step == 0 or step % self.update_interval != 0:
            return

        rows = len(self.static_grid)
        cols = len(self.static_grid[0])
        forbidden = {predator_pos, prey_pos}

        if not self.obstacles:
            action = "add"
        elif len(self.obstacles) >= self.max_obstacles:
            action = "remove"
        else:
            action = self._rng.choice(["add", "add", "remove"])

        if action == "remove":
            # sorted để đảm bảo thứ tự deterministic
            victim = self._rng.choice(sorted(self.obstacles))
            self.obstacles.discard(victim)
            self._dirty = True
        else:
            free = [
                (r, c)
                for r in range(rows)
                for c in range(cols)
                if self.static_grid[r][c] == 0
                and (r, c) not in forbidden
                and (r, c) not in self.obstacles
            ]
            if free:
                new_obs = self._rng.choice(free)
                self.obstacles.add(new_obs)
                self._dirty = True

    def get_effective_grid(self) -> list[list[int]]:
        """
        Trả về bản sao grid với vật cản động được đánh dấu bằng OBSTACLE_VALUE (2).
        Kết quả được cache lại đến lần update tiếp theo.
        """
        if not self._dirty and self._cached_grid is not None:
            return self._cached_grid

        grid = [row[:] for row in self.static_grid]
        for r, c in self.obstacles:
            grid[r][c] = self.OBSTACLE_VALUE

        self._cached_grid = grid
        self._dirty = False
        return grid

    def reset(self) -> None:
        """Khởi tạo lại toàn bộ về trạng thái ban đầu (cùng seed)."""
        self._rng = random.Random(self.seed)
        self.obstacles = set()
        self._dirty = True
        self._cached_grid = None
