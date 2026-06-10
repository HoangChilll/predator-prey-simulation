from collections import deque
import heapq
from algorithm.visited_tracker import set_visited

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # lên, xuống, trái, phải


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def is_free(grid, r, c):
    return in_bounds(grid, r, c) and grid[r][c] == 0

def neighbors(grid, r, c):
    return [(r + dr, c + dc) for dr, dc in DIRS if is_free(grid, r + dr, c + dc)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def bfs_dist(grid, start, blocked=None):
    blocked = blocked or set()
    dist = {}
    if not is_free(grid, *start) or start in blocked:
        return dist
    dist[start] = 0
    q = deque([start])
    while q:
        r, c = q.popleft()
        for nb in neighbors(grid, r, c):
            if nb not in dist and nb not in blocked:
                dist[nb] = dist[(r, c)] + 1
                q.append(nb)
    return dist



def flood_area(grid, start, blocked, cap=120):
    if start in blocked or not is_free(grid, *start):
        return 0
    seen = {start}
    q = deque([start])
    n = 0
    while q and n < cap:
        r, c = q.popleft()
        n += 1
        for nb in neighbors(grid, r, c):
            if nb not in seen and nb not in blocked:
                seen.add(nb)
                q.append(nb)
    return n



def a_star(grid, start, goal):
    if start == goal:
        return [start]
    open_heap = [(manhattan(start, goal), 0, start)]
    came, g = {}, {start: 0}
    while open_heap:
        _, gc, cur = heapq.heappop(open_heap)
        if cur == goal:
            path = [cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            return path[::-1]
        if gc > g.get(cur, 1e18):
            continue
        for nb in neighbors(grid, *cur):
            ng = gc + 1
            if ng < g.get(nb, 1e18):
                g[nb] = ng
                came[nb] = cur
                heapq.heappush(open_heap, (ng + manhattan(nb, goal), ng, nb))
    return []



W = dict(DIST=2.4, SPACE=1.5, EXIT=1.0, VOR=0.5, WALL=1.0, DANGER=9.0)

def evade(grid, self_pos, opponent_pos, last_dir=None, pred_speed=2):
    pred_field = bfs_dist(grid, opponent_pos)
    big = len(grid) * len(grid[0])

    pred_path = a_star(grid, opponent_pos, self_pos)

    danger = {opponent_pos}
    for i in range(1, pred_speed + 1):
        node = pred_path[i] if len(pred_path) > i else (pred_path[-1] if pred_path else opponent_pos)
        danger.add(node)
    pred_last = pred_path[pred_speed] if len(pred_path) > pred_speed else (
                pred_path[-1] if pred_path else opponent_pos)
    danger |= set(neighbors(grid, *pred_last))

    candidates = neighbors(grid, *self_pos)
    best, best_score = None, float("-inf")

    for c in candidates:
        if c == opponent_pos:
            continue
        pd = pred_field.get(c, float("inf"))
        if pd <= pred_speed and len(candidates) > 1:
            continue
        pd_eff = pd if pd != float("inf") else big

        space = flood_area(grid, c, danger, cap=120)
        exits = len(neighbors(grid, *c))
        my_field = bfs_dist(grid, c)
        owned = sum(1 for cell, d in my_field.items()
                    if d * pred_speed < pred_field.get(cell, float("inf")))
        walls = sum(1 for dr, dc in DIRS if not is_free(grid, c[0] + dr, c[1] + dc))

        score = (W["DIST"] * pd_eff + W["SPACE"] * space + W["EXIT"] * exits
                 + W["VOR"] * owned - W["WALL"] * walls)
        if c in danger:
            score -= W["DANGER"]

        if score > best_score:
            best_score, best = score, c

    if best is None:
        best = self_pos

    return best


# thuật toán A* mặc định (fallback)
def astar_flee(grid, self_pos, opponent_pos):
    pred_field = bfs_dist(grid, opponent_pos)
    my_field = bfs_dist(grid, self_pos)
    big = len(grid) * len(grid[0])
    target, best = self_pos, -1
    for cell in my_field:
        pd = pred_field.get(cell, big)
        if pd > best:
            best, target = pd, cell
    path = a_star(grid, self_pos, target)
    return path[1] if len(path) > 1 else self_pos


# thuật toán chính

def prey_move(grid, self_pos, opponent_pos, last_dir=None, pred_speed=2):
    nxt = evade(grid, self_pos, opponent_pos, last_dir, pred_speed)
    if nxt is None:
        nxt = astar_flee(grid, self_pos, opponent_pos)
    return nxt


def prey_weighted_evade(grid, self_pos, opponent_pos, last_dir=None, pred_speed=2):
    nxt = evade(grid, self_pos, opponent_pos, last_dir, pred_speed)
    if nxt is None:
        nxt = astar_flee(grid, self_pos, opponent_pos)
    # Ghi visited: các ô lân cận được cân nhắc + bước đi tiếp theo
    visited_cells = [self_pos] + [
        (self_pos[0] + dr, self_pos[1] + dc)
        for dr, dc in DIRS
        if 0 <= self_pos[0]+dr < len(grid) and 0 <= self_pos[1]+dc < len(grid[0])
        and grid[self_pos[0]+dr][self_pos[1]+dc] == 0
    ]
    set_visited(visited_cells, [self_pos, nxt] if nxt != self_pos else [self_pos])
    return nxt

