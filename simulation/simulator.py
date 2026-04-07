import random

class Simulator:
    def __init__(self, grid, predator_strategy, prey_strategy):
        self.grid = grid

        # 🔥 strategy
        self.predator_strategy = predator_strategy
        self.prey_strategy = prey_strategy

        # agents
        self.predators = []
        self.preys = []

        # predator move counter
        self.predator_steps = 0

    # =========================
    # ADD AGENTS
    # =========================
    def add_predator(self, x, y):
        if self.grid.place_predator(x, y):
            self.predators.append((x, y))

    def add_prey(self, x, y):
        if self.grid.place_prey(x, y):
            self.preys.append((x, y))

    # =========================
    # HELPER
    # =========================
    def get_neighbors(self, x, y):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        result = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.grid.in_bounds(nx, ny) and self.grid.is_walkable(nx, ny):
                result.append((nx, ny))

        return result

    # =========================
    # STEP LOGIC
    # =========================
    def step(self):

        # =====================
        # PREY MOVE
        # =====================
        new_preys = []

        for (x, y) in self.preys:

            # 🔥 gọi strategy
            move = self.prey_strategy.get_move(
                (x, y),
                self,
                targets=self.predators   # prey né predator
            )

            if move:
                nx, ny = move
                if self.grid.get(nx, ny) == self.grid.EMPTY:
                    self.grid.move(x, y, nx, ny)
                    new_preys.append((nx, ny))
                else:
                    new_preys.append((x, y))
            else:
                new_preys.append((x, y))

        self.preys = new_preys

        # =====================
        # PREDATOR MOVE
        # =====================
        new_predators = []
        new_preys_after_eat = self.preys.copy()

        for (x, y) in self.predators:

            # 🔥 gọi strategy
            move = self.predator_strategy.get_move(
                (x, y),
                self,
                targets=self.preys   # predator đuổi prey
            )

            if move:
                nx, ny = move
                cell = self.grid.get(nx, ny)

                # ăn prey
                if cell == self.grid.PREY:
                    self.grid.move(x, y, nx, ny)

                    if (nx, ny) in new_preys_after_eat:
                        new_preys_after_eat.remove((nx, ny))

                    new_predators.append((nx, ny))

                # đi vào ô trống
                elif cell == self.grid.EMPTY:
                    self.grid.move(x, y, nx, ny)
                    new_predators.append((nx, ny))

                else:
                    new_predators.append((x, y))
            else:
                new_predators.append((x, y))

        self.predators = new_predators
        self.preys = new_preys_after_eat

        # sau mỗi bước di chuyển của predator tăng bộ đếm
        self.predator_steps += 1
