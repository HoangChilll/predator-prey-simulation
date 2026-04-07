from agents.base_agent import BaseAgent


class Prey(BaseAgent):
    def __init__(self, position, strategy):
        super().__init__(position)

        self.strategy = strategy
        self.type = "prey"
        self.alive = True

    # =========================
    # CHỌN HÀNH ĐỘNG
    # =========================
    def choose_action(self, grid):
        if not self.alive:
            return None

        return self.strategy.get_action(self, grid)

    # =========================
    # RESET
    # =========================
    def reset(self):
        self.alive = True
        if hasattr(self, "initial_position"):
            self.position = self.initial_position