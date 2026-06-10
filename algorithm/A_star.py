import heapq
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited


def predator_astar(grid, self_pos, opponent_pos):
    
    start = tuple(self_pos)
    goal  = tuple(opponent_pos)

    if start == goal:
        return start

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # (f_score, g_score, vị_trí, đường_đi)
    open_heap     = [(heuristic(start, goal), 0, start, [start])]
    g_score       = {start: 0}
    visited_order = []

    while open_heap:
        f, g, current, path = heapq.heappop(open_heap)

        # Bỏ qua nếu đã tìm được đường ngắn hơn đến current
        if g > g_score.get(current, float('inf')):
            continue

        visited_order.append(current)

        # Tới Prey thì dừng
        if current == goal:
            set_visited(visited_order, path)
            return path[1] if len(path) > 1 else start

        x, y = current
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)
            if not is_valid(neighbor, grid):
                continue
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                f_new = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_new, tentative_g, neighbor, path + [neighbor]))

    # Không tìm được đường → đứng yên
    set_visited(visited_order, [])
    return start