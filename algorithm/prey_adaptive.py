from collections import deque
import heapq
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited

# ----------------------------------------------------------------------
# Tiện ích cơ bản
# ----------------------------------------------------------------------

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs_dist(grid, start, blocked=None):
    """
    BFS từ start, trả về dict {pos: distance} tới mọi ô đến được.
    blocked: tập ô coi như tường (thường là vị trí Predator).
    """
    if blocked is None:
        blocked = set()
    dist = {}
    if not is_valid(start, grid) or start in blocked:
        return dist
    dist[start] = 0
    q = deque([start])
    while q:
        pos = q.popleft()
        x, y = pos
        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in dist and nxt not in blocked and is_valid(nxt, grid):
                dist[nxt] = dist[pos] + 1
                q.append(nxt)
    return dist


def flood_fill(grid, start, blocked=None, cap=200):
    """
    Flood fill từ start, trả về số ô đến được.
    cap: giới hạn đếm để tránh tốn thời gian trên map lớn.
    """
    if blocked is None:
        blocked = set()
    if not is_valid(start, grid) or start in blocked:
        return 0
    seen = {start}
    q = deque([start])
    n = 0
    while q and n < cap:
        x, y = q.popleft()
        n += 1
        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in seen and nxt not in blocked and is_valid(nxt, grid):
                seen.add(nxt)
                q.append(nxt)
    return n


def get_neighbors(grid, pos):
    x, y = pos
    return [
        (x + dx, y + dy)
        for dx, dy in DIRECTIONS
        if is_valid((x + dx, y + dy), grid)
    ]


# ----------------------------------------------------------------------
# A* — tìm đường ngắn nhất (dùng làm công cụ phụ và fallback)
# ----------------------------------------------------------------------

def a_star(grid, start, goal, blocked=None):
    """
    Trả về danh sách ô từ start -> goal (rỗng nếu không tìm được).
    """
    if blocked is None:
        blocked = set()
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
        if gc > g.get(cur, float('inf')):
            continue
        for nb in get_neighbors(grid, cur):
            if nb in blocked:
                continue
            ng = gc + 1
            if ng < g.get(nb, float('inf')):
                g[nb] = ng
                came[nb] = cur
                heapq.heappush(open_heap, (ng + manhattan(nb, goal), ng, nb))
    return []


# ----------------------------------------------------------------------
# Articulation Points — phát hiện ngõ cụt (từ File 1)
# ----------------------------------------------------------------------

def find_articulation_points(grid, start, blocked=None):
    """
    Tìm articulation points (điểm thắt cổ chai) trong vùng Prey có thể đến.
    Dùng Tarjan iterative để tránh RecursionError trên map lớn.
    AP = ô mà nếu đi qua đó, Prey có thể bị nhốt vào vùng nhỏ hơn.
    """
    if blocked is None:
        blocked = set()

    # Chỉ xét ô Prey có thể đến được
    reachable_set = set()
    q = deque([start])
    reachable_set.add(start)
    while q:
        x, y = q.popleft()
        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in reachable_set and nxt not in blocked and is_valid(nxt, grid):
                reachable_set.add(nxt)
                q.append(nxt)

    if not reachable_set:
        return set()

    visited = {}
    low     = {}
    parent  = {}
    ap      = set()
    timer   = [0]

    def dfs_iterative(root):
        stack = [(root, iter([
            (root[0] + dx, root[1] + dy)
            for dx, dy in DIRECTIONS
            if (root[0] + dx, root[1] + dy) in reachable_set
        ]), [0])]
        visited[root] = low[root] = timer[0]
        timer[0] += 1
        parent[root] = None

        while stack:
            u, neighbors_iter, child_count = stack[-1]
            try:
                v = next(neighbors_iter)
                if v not in reachable_set:
                    continue
                if v not in visited:
                    visited[v] = low[v] = timer[0]
                    timer[0] += 1
                    parent[v] = u
                    child_count[0] += 1
                    stack.append((v, iter([
                        (v[0] + dx, v[1] + dy)
                        for dx, dy in DIRECTIONS
                        if (v[0] + dx, v[1] + dy) in reachable_set
                    ]), [0]))
                elif v != parent[u]:
                    low[u] = min(low[u], visited[v])
            except StopIteration:
                stack.pop()
                if stack:
                    pu = stack[-1][0]
                    low[pu] = min(low[pu], low[u])
                    if parent[pu] is None:
                        if stack[-1][2][0] > 1:
                            ap.add(pu)
                    else:
                        if low[u] >= visited[pu]:
                            ap.add(pu)

    dfs_iterative(start)
    return ap


def component_size_after_crossing(grid, crossing_pos, from_pos, blocked=None):
    """
    Nếu Prey bước từ from_pos sang crossing_pos (một AP),
    vùng phía sau crossing_pos có bao nhiêu ô?
    Dùng để quyết định: "Ngõ kia tuy là AP nhưng vẫn rộng không?"
    """
    if blocked is None:
        blocked = set()
    blocked_sim = blocked | {from_pos}
    return flood_fill(grid, crossing_pos, blocked=blocked_sim)


# ----------------------------------------------------------------------
# Trọng số động theo khoảng cách Predator
# ----------------------------------------------------------------------

def get_dynamic_weights(dist_to_pred):
    """
    Điều chỉnh trọng số theo mức độ nguy hiểm:
      - Gần (<=3): ưu tiên chạy xa tối đa
      - Trung bình (<=6): cân bằng
      - An toàn (>6): ưu tiên giữ không gian sống
    """
    if dist_to_pred <= 3:
        return dict(DIST=3.0, SPACE=1.0, EXIT=0.8, VOR=0.3, AP_PEN=2.0, DANGER=12.0)
    elif dist_to_pred <= 6:
        return dict(DIST=2.0, SPACE=1.5, EXIT=1.0, VOR=0.5, AP_PEN=1.5, DANGER=9.0)
    else:
        return dict(DIST=1.0, SPACE=2.5, EXIT=1.0, VOR=0.8, AP_PEN=0.8, DANGER=6.0)


# ----------------------------------------------------------------------
# Fallback: A* chạy đến ô xa Predator nhất
# ----------------------------------------------------------------------

def astar_flee(grid, self_pos, opponent_pos):
    """
    Fallback khi evade() không tìm được bước đi.
    Dùng A* chạy đến ô xa Predator nhất.
    """
    pred_field = bfs_dist(grid, opponent_pos)
    my_field   = bfs_dist(grid, self_pos)
    big        = len(grid) * len(grid[0])

    target, best = self_pos, -1
    for cell in my_field:
        pd = pred_field.get(cell, big)
        if pd > best:
            best, target = pd, cell

    path = a_star(grid, self_pos, target)
    return path[1] if len(path) > 1 else self_pos


# ----------------------------------------------------------------------
# Hàm chính — Prey adaptive
# ----------------------------------------------------------------------

def evade_adaptive(grid, self_pos, opponent_pos, pred_speed=2):
    """
    Chiến lược kết hợp File 1 (AP check) + File 3 (danger zone + weighted score).

    Pipeline:
      1. Xây dựng danger zone từ pred_speed bước tiếp theo của Predator
      2. Tính trọng số động theo khoảng cách thực tế đến Predator
      3. Tìm Articulation Points để phát hiện ngõ cụt
      4. Đánh giá từng bước đi:
           - Hard filter: loại ô nằm trong tầm Predator (pd <= pred_speed)
           - AP penalty: phạt nặng nếu bước vào AP dẫn vùng quá nhỏ
           - Score tổng hợp: DIST + SPACE + EXIT + VOR - AP_PEN - DANGER
      5. Fallback astar_flee nếu không có bước hợp lệ

    Args:
        grid:         bản đồ game
        self_pos:     vị trí Prey hiện tại
        opponent_pos: vị trí Predator hiện tại
        pred_speed:   số bước Predator đi được trong 1 lượt

    Returns:
        tuple (x, y) — vị trí Prey sẽ di chuyển đến
    """
    prey_pos = self_pos
    pred_pos = opponent_pos

    # --- Khoảng cách thực tế (BFS) ---
    pred_field = bfs_dist(grid, pred_pos)
    dist_real  = pred_field.get(prey_pos, 999)

    # --- Danger zone: các ô Predator sẽ chiếm trong pred_speed bước ---
    pred_path = a_star(grid, pred_pos, prey_pos)
    danger = {pred_pos}
    for i in range(1, pred_speed + 1):
        if len(pred_path) > i:
            danger.add(pred_path[i])
        elif pred_path:
            danger.add(pred_path[-1])
    # Thêm lân cận bước cuối của Predator
    if pred_path:
        pred_last = pred_path[pred_speed] if len(pred_path) > pred_speed else pred_path[-1]
        for nb in get_neighbors(grid, pred_last):
            danger.add(nb)

    # --- Trọng số động ---
    W = get_dynamic_weights(dist_real)

    # --- Articulation Points ---
    art_points = find_articulation_points(grid, prey_pos, blocked={pred_pos})

    # --- Ngưỡng ngõ cụt ---
    DEAD_END_THRESHOLD = 8

    # --- Các bước đi hợp lệ ---
    candidates = get_neighbors(grid, prey_pos)
    visited_cells = [prey_pos] + [c for c in candidates if c != pred_pos]
    if not candidates:
        set_visited([prey_pos], [prey_pos])
        return prey_pos

    scored = []

    for c in candidates:
        if c == pred_pos:
            continue

        pd = pred_field.get(c, 999)

        # Hard filter: loại ô nằm trong tầm Predator
        if pd <= pred_speed and len(candidates) > 1:
            continue

        # --- AP penalty (từ File 1) ---
        ap_penalty = 0.0
        if c in art_points:
            size_behind = component_size_after_crossing(
                grid, c, from_pos=prey_pos, blocked={pred_pos}
            )
            if size_behind < DEAD_END_THRESHOLD:
                # Ngõ cụt thực sự → phạt rất nặng
                ap_penalty = (DEAD_END_THRESHOLD - size_behind) * 10
            else:
                # AP nhưng vùng sau còn rộng → phạt nhẹ
                ap_penalty = 2.0

        # --- Các chỉ số đánh giá ---
        space  = flood_fill(grid, c, blocked=danger)       # vùng sống tránh danger
        exits  = len(get_neighbors(grid, c))               # số lối thoát
        pd_eff = pd if pd != float('inf') else 999

        # Voronoi: ô Prey đến trước Predator (tính theo tốc độ)
        my_field = bfs_dist(grid, c)
        owned = sum(
            1 for cell, d in my_field.items()
            if d * pred_speed < pred_field.get(cell, float('inf'))
        )

        # --- Score tổng hợp (cao hơn = tốt hơn) ---
        score = (
              W["DIST"]  * pd_eff
            + W["SPACE"] * space
            + W["EXIT"]  * exits
            + W["VOR"]   * owned
            - W["AP_PEN"] * ap_penalty
        )

        # Phạt thêm nếu bước vào vùng nguy hiểm
        if c in danger:
            score -= W["DANGER"]

        scored.append((score, c, space, ap_penalty))
        print(f"  [Prey] cân nhắc {c}: pd={pd}, space={space}, "
              f"exits={exits}, voronoi={owned}, "
              f"ap_penalty={ap_penalty:.1f}, score={score:.2f}")

    if not scored:
        print("[Prey] Không có bước hợp lệ → fallback astar_flee")
        fallback = astar_flee(grid, prey_pos, pred_pos)
        set_visited([prey_pos], [prey_pos, fallback])
        return fallback

    score_map = {cell: score for score, cell, _, _ in scored}

    # --- Ưu tiên bước không phải ngõ cụt thực sự ---
    safe = [(s, c, a, p) for s, c, a, p in scored if p < 5.0]

    if safe:
        best = max(safe, key=lambda x: x[0])
    else:
        # Mọi bước đều nguy hiểm → chọn vùng sống lớn nhất
        best = max(scored, key=lambda x: x[2])
        print("[Prey] Mọi bước đều là AP/ngõ cụt → chọn vùng lớn nhất")

    chosen = best[1]
    print(f"[Prey] pos={prey_pos} -> move={chosen} | "
          f"space={best[2]} | ap_penalty={best[3]:.1f} | score={best[0]:.2f} | "
          f"dist_pred={dist_real} | weights=DIST:{W['DIST']}/SPACE:{W['SPACE']}")

    set_visited(visited_cells, [prey_pos, chosen], scores=score_map)
    return chosen


# ----------------------------------------------------------------------
# Entry point (thay thế prey_A_star_ap của File 1)
# ----------------------------------------------------------------------

def prey_adaptive(grid, self_pos, opponent_pos, pred_speed=2):
    """
    Hàm chính thay thế prey_A_star_ap (File 1).

    Kết hợp:
      - Danger zone + pred_speed awareness (File 3)
      - Articulation Point check (File 1)
      - Trọng số động theo khoảng cách (mới)
      - astar_flee fallback (File 3)
    """
    nxt = evade_adaptive(grid, self_pos, opponent_pos, pred_speed)
    if nxt is None:
        nxt = astar_flee(grid, self_pos, opponent_pos)
    return nxt