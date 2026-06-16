import random


class DynamicObstacleManager:

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

 

    def update(self, step: int, predator_pos: tuple, prey_pos: tuple) -> None:
        #Gọi sau mỗi bước sim.
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
            # sorted để đảm bảo thứ tự cố định khi chọn ngẫu nhiên, giúp tái tạo kết quả nhất quán
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
        #trả về bản sao cùng đánh dấu vật cản động.
        if not self._dirty and self._cached_grid is not None:
            return self._cached_grid

        grid = [row[:] for row in self.static_grid]
        for r, c in self.obstacles:
            grid[r][c] = self.OBSTACLE_VALUE

        self._cached_grid = grid
        self._dirty = False
        return grid

    def reset(self) -> None:
        #trạng thái ban đầu 
        self._rng = random.Random(self.seed)
        self.obstacles = set()
        self._dirty = True
        self._cached_grid = None
