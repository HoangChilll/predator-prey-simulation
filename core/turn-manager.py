class TurnManager:
    def __init__(self, agents):
        self.agents = agents      # list agent
        self.index = 0            # agent hiện tại
        self.round = 0            # số vòng đã chơi

    # =========================
    # AGENT HIỆN TẠI
    # =========================
    def current_agent(self):
        if not self.agents:
            return None
        return self.agents[self.index]

    # =========================
    # CHUYỂN TURN
    # =========================
    def next_turn(self):
        if not self.agents:
            return

        self.index += 1

        # hết 1 vòng
        if self.index >= len(self.agents):
            self.index = 0
            self.round += 1

    # =========================
    # RESET
    # =========================
    def reset(self):
        self.index = 0
        self.round = 0

    # =========================
    # THÊM / XOÁ AGENT
    # =========================
    def add_agent(self, agent):
        self.agents.append(agent)

    def remove_agent(self, agent):
        if agent in self.agents:
            idx = self.agents.index(agent)
            self.agents.remove(agent)

            # fix index nếu cần
            if idx <= self.index and self.index > 0:
                self.index -= 1

    # =========================
    # DEBUG / INFO
    # =========================
    def get_turn_info(self):
        return {
            "current_index": self.index,
            "round": self.round,
            "total_agents": len(self.agents)
        }