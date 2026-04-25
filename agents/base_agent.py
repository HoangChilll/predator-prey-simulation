class BaseAgent:
    def __init__(self, position):
        self.position = position
        self.initial_position = position

    def choose_action(self, grid):
        raise NotImplementedError