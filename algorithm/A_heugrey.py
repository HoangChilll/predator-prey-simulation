from collections import deque
import heapq

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # lên, xuống, trái, phải

# Predator (prey trong game) di 2 buoc/luot, grey di 1 buoc/luot
PRED_SPEED = 2

# ----------------------------------------------------------------------
# Tiện ích lưới
# ----------------------------------------------------------------------
def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def is_free(grid, r, c):
    return in_bounds(grid, r, c) and grid[r][c] == 0

def neighbors(grid, r, c):
    return [(r + dr, c + dc) for dr, dc in DIRS if is_free(grid, r + dr, c + dc)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ----------------------------------------------------------------------
# BFS: khoảng cách ĐƯỜNG-ĐI-THẬT từ 'start' tới mọi ô tới được
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Flood fill: đếm số ô trống tới được từ 'start' (coi 'blocked' là tường).
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# A*: đường ngắn nhất start -> goal. Trả về danh sách ô (rỗng nếu bí).
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# NÉ THÔNG MINH (logic chính)
# FIX: tính đúng tốc độ predator (PRED_SPEED = 2 bước/lượt)
#   - Vùng nguy hiểm = PRED_SPEED bước tiếp theo của predator + lân cận
#   - Ngưỡng lọc: pd <= PRED_SPEED (predator đến được trong 1 lượt grey)
#   - Voronoi: grey cần tới trước predator tính theo tốc độ thực
# ----------------------------------------------------------------------
W = dict(DIST=2.4, SPACE=1.5, EXIT=1.0, VOR=0.5, WALL=1.0, DANGER=9.0, MOMENTUM=2.5)

def evade(grid, self_pos, opponent_pos, last_dir=None):
    pred_field = bfs_dist(grid, opponent_pos)               # đường thật predator -> mọi ô
    big = len(grid) * len(grid[0])

    # Dự đoán PRED_SPEED bước của predator (predator di 2 ô/lượt)
    pred_path = a_star(grid, opponent_pos, self_pos)

    # Vùng nguy hiểm = tất cả ô predator đi qua trong PRED_SPEED bước + lân cận bước cuối
    danger = {opponent_pos}
    for i in range(1, PRED_SPEED + 1):
        node = pred_path[i] if len(pred_path) > i else (pred_path[-1] if pred_path else opponent_pos)
        danger.add(node)
    pred_last = pred_path[PRED_SPEED] if len(pred_path) > PRED_SPEED else (
                pred_path[-1] if pred_path else opponent_pos)
    danger |= set(neighbors(grid, *pred_last))

    candidates = neighbors(grid, *self_pos)                  # chỉ 4 hướng, KHÔNG đứng yên
    best, best_score = None, float("-inf")

    for c in candidates:
        if c == opponent_pos:
            continue
        pd = pred_field.get(c, float("inf"))
        # Predator đi PRED_SPEED bước/lượt → né ô predator có thể đến trong 1 lượt
        if pd <= PRED_SPEED and len(candidates) > 1:
            continue
        pd_eff = pd if pd != float("inf") else big          # predator không tới được = rất an toàn

        space = flood_area(grid, c, danger, cap=120)        # không gian mở (anti ngõ cụt)
        exits = len(neighbors(grid, *c))                    # số lối thoát
        my_field = bfs_dist(grid, c)
        # Voronoi: grey đến trước predator tính theo tốc độ thực (predator nhanh 2x)
        owned = sum(1 for cell, d in my_field.items()
                    if d * PRED_SPEED < pred_field.get(cell, float("inf")))
        walls = sum(1 for dr, dc in DIRS if not is_free(grid, c[0] + dr, c[1] + dc))
        step = (c[0] - self_pos[0], c[1] - self_pos[1])
        mom = 1 if (last_dir and step == last_dir) else 0   # giữ đà -> lượn mượt

        score = (W["DIST"] * pd_eff + W["SPACE"] * space + W["EXIT"] * exits
                 + W["VOR"] * owned - W["WALL"] * walls + W["MOMENTUM"] * mom)
        if c in danger:
            score -= W["DANGER"]                            # ô predator sắp tới: trừ nặng

        if score > best_score:
            best_score, best = score, c

    # Nếu tất cả neighbors bị lọc (bí hoàn toàn) → đứng yên như last resort
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
def grey_move(grid, self_pos, opponent_pos, last_dir=None):
    nxt = evade(grid, self_pos, opponent_pos, last_dir)     # thuật toán chính
    if nxt is None:
        nxt = astar_flee(grid, self_pos, opponent_pos)      # fallback A*
    return nxt
