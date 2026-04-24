class DFSStrategy:
    def __init__(self):
        self.nodes_expanded = 0

    def get_action(self, state):
        """
        Trả về action (dx, dy) cho bước tiếp theo
        """
        start = state.pacman

        # 👉 Tạm thời target là ghost (bạn có thể đổi sang food)
        goal = state.ghost

        # Stack: (position, path)
        stack = [(start, [])]
        visited = set()

        self.nodes_expanded = 0

        while stack:
            current, path = stack.pop()
            self.nodes_expanded += 1

            if current == goal:
                if path:
                    return path[0]  # chỉ lấy bước đầu tiên
                return (0, 0)

            if current in visited:
                continue

            visited.add(current)

            for move in self.get_neighbors(current, state):
                nx = current[0] + move[0]
                ny = current[1] + move[1]
                next_pos = (nx, ny)

                if next_pos not in visited:
                    stack.append((next_pos, path + [move]))

        # nếu không tìm được đường
        return (0, 0)

    def get_neighbors(self, pos, state):
        """
        Trả về list các hướng đi hợp lệ (dx, dy)
        """
        directions = [
            (0, 1),   # xuống
            (1, 0),   # phải
            (0, -1),  # lên
            (-1, 0)   # trái
        ]

        valid_moves = []

        for dx, dy in directions:
            nx = pos[0] + dx
            ny = pos[1] + dy

            # check không đâm tường
            if not state.is_wall(nx, ny):
                valid_moves.append((dx, dy))

        return valid_moves