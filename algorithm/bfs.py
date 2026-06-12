from collections import deque
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited

def predator_bfs(grid, self_pos, opponent_pos):
    
    start = tuple(self_pos)
    goal  = tuple(opponent_pos)
    queue         = deque([(start, [start])])
    visited       = {start}   # đánh dấu ngay khi thêm vào queue
    visited_order = []

    while queue:
        current, path = queue.popleft()  
        visited_order.append(current)

        # Tới Prey thì dừng
        if current == goal:
            set_visited(visited_order, path)
            # Trả về bước đầu tiên sau start
            return path[1] if len(path) > 1 else start

        x, y = current
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)
            if is_valid(neighbor, grid) and neighbor not in visited:
                visited.add(neighbor)   # đánh dấu sớm, tránh thêm trùng
                queue.append((neighbor, path + [neighbor]))

    # Không tìm được đường
    set_visited(visited_order, [])
    return start