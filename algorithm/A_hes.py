import heapq
from collections import deque
from algorithm.selectalgorithm import is_valid,DIRECTIONS
 
 
# ============================================================
# BƯỚC 1: Flood Fill — đếm "không gian sống" của Grey
# ============================================================
def flood_fill(grid, start, blocked=None):
    """
    Xuất phát từ 'start', lan ra tất cả ô có thể đến được
    (như đổ nước — dừng lại ở tường hoặc ô bị chặn).
 
    Args:
        grid:    bản đồ game
        start:   vị trí xuất phát (tuple x, y)
        blocked: tập hợp các ô coi như bị chặn (vd: vị trí Predator)
 
    Returns:
        set các ô có thể đến được từ start
    """
    if blocked is None:
        blocked = set()
 
    visited = {start}
    queue = deque([start])
 
    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in visited and nxt not in blocked and is_valid(nxt, grid):
                visited.add(nxt)
                queue.append(nxt)
 
    return visited  # tổng số ô = len(visited) = "không gian sống"
 
 
# ============================================================
# BƯỚC 2: Tìm Articulation Points (điểm thắt cổ chai)
# ============================================================
def find_articulation_points(grid, start, blocked=None):
    """
    Tìm tất cả articulation points trong vùng Grey có thể đến.
    Dùng thuật toán Tarjan (DFS iterative để tránh RecursionError).
 
    Articulation point = ô mà nếu xóa đi thì vùng bị chia làm 2 phần riêng.
    → Đây là nơi Predator cần chặn để nhốt Grey.
 
    Args:
        grid:    bản đồ game
        start:   vị trí Grey
        blocked: ô bị chặn (vd: vị trí Predator)
 
    Returns:
        set các articulation points
    """
    if blocked is None:
        blocked = set()
 
    # Chỉ xét các ô Grey có thể đến được
    reachable = flood_fill(grid, start, blocked)
    if not reachable:
        return set()
 
    # Tarjan iterative
    visited = {}   # thứ tự DFS vào ô
    low     = {}   # ô thấp nhất có thể lên được qua back-edge
    parent  = {}
    ap      = set()
    timer   = [0]
 
    def dfs_iterative(root):
        stack = [(root, iter([
            (root[0]+dx, root[1]+dy)
            for dx, dy in DIRECTIONS
            if (root[0]+dx, root[1]+dy) in reachable
        ]), [0])]
        visited[root] = low[root] = timer[0]
        timer[0] += 1
        parent[root] = None
 
        while stack:
            u, neighbors, child_count = stack[-1]
            try:
                v = next(neighbors)
                if v not in reachable:
                    continue
                if v not in visited:
                    # Đi xuống
                    visited[v] = low[v] = timer[0]
                    timer[0] += 1
                    parent[v] = u
                    child_count[0] += 1
                    stack.append((v, iter([
                        (v[0]+dx, v[1]+dy)
                        for dx, dy in DIRECTIONS
                        if (v[0]+dx, v[1]+dy) in reachable
                    ]), [0]))
                elif v != parent[u]:
                    # Back-edge
                    low[u] = min(low[u], visited[v])
            except StopIteration:
                # Quay lên
                stack.pop()
                if stack:
                    pu = stack[-1][0]
                    low[pu] = min(low[pu], low[u])
                    # Kiểm tra AP
                    if parent[pu] is None:
                        # pu là root → AP nếu có ≥ 2 con
                        if stack[-1][2][0] > 1:
                            ap.add(pu)
                    else:
                        if low[u] >= visited[pu]:
                            ap.add(pu)
 
    dfs_iterative(start)
    return ap
 
 
# ============================================================
# BƯỚC 3: A* tìm đường ngắn nhất
# ============================================================
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
 
 
def astar_next_step(grid, start, goal, blocked=None):
    """
    Dùng A* tìm bước đi tiếp theo từ start đến goal.
    Trả về ô kế tiếp trên đường đi ngắn nhất (không phải toàn bộ path).
 
    Args:
        grid:    bản đồ game
        start:   vị trí hiện tại của Predator
        goal:    đích muốn đến (Grey hoặc articulation point)
        blocked: ô không được đi qua
 
    Returns:
        tuple (x, y) — bước tiếp theo; hoặc start nếu không có đường
    """
    if blocked is None:
        blocked = set()
 
    if start == goal:
        return start
 
    # (f_score, g_score, vị_trí)
    open_heap = [(manhattan(start, goal), 0, start)]
    g_score   = {start: 0}
    came_from = {}
 
    while open_heap:
        f, g, current = heapq.heappop(open_heap)
 
        if current == goal:
            # Truy vết về bước đầu tiên
            while came_from.get(current) != start:
                current = came_from[current]
                if current not in came_from:
                    return start
            return current
 
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if not is_valid(neighbor, grid) or neighbor in blocked:
                continue
            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor]   = tentative_g
                f_new = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_heap, (f_new, tentative_g, neighbor))
 
    return start  # Không tìm được đường
 
 
# thuật toán cho kẻ săn mồi 
def _bfs_dist(grid, start, goal):
    """BFS distance từ start đến goal, trả về inf nếu không đến được."""
    if start == goal:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        pos, d = queue.popleft()
        for dx, dy in DIRECTIONS:
            nxt = (pos[0] + dx, pos[1] + dy)
            if nxt == goal:
                return d + 1
            if nxt not in visited and is_valid(nxt, grid):
                visited.add(nxt)
                queue.append((nxt, d + 1))
    return float('inf')


def _get_optimize_move(grid, pred_pos, grey_pos, valid_moves):
    """
    Tìm bước đi tối ưu giảm vùng sống của Grey.

    Thử theo thứ tự:
      1. AP — chặn điểm thắt cổ chai mà Predator đến trước Grey.
      2. Shrink — bước đi thu hẹp tối đa diện tích Grey có thể đến.

    Returns:
        tuple (x, y) nếu tối ưu được, None nếu không thể.
    """
    # Chiến lược 1: AP
    art_points = find_articulation_points(grid, grey_pos, blocked={pred_pos})
    valuable_aps = [
        ap for ap in art_points
        if _bfs_dist(grid, pred_pos, ap) <= _bfs_dist(grid, grey_pos, ap)
    ]

    if valuable_aps:
        best_ap = min(valuable_aps, key=lambda ap: _bfs_dist(grid, grey_pos, ap))
        next_step = astar_next_step(grid, pred_pos, best_ap)
        if next_step != pred_pos:
            # Chỉ dùng AP nếu bước đó không làm predator xa grey hơn
            if _bfs_dist(grid, next_step, grey_pos) <= _bfs_dist(grid, pred_pos, grey_pos):
                print(f"[Predator] AP={best_ap} | pos={pred_pos} -> step={next_step}")
                return next_step

    # Chiến lược 2: Shrink
    current_grey_area = len(flood_fill(grid, grey_pos, blocked={pred_pos}))
    best_move = None
    best_reduction = 0

    for move in valid_moves:
        new_grey_area = len(flood_fill(grid, grey_pos, blocked={move}))
        reduction = current_grey_area - new_grey_area
        if reduction > best_reduction:
            best_reduction = reduction
            best_move = move

    if best_move is not None:
        print(f"[Predator] SHRINK | pos={pred_pos} -> move={best_move} | reduction={best_reduction}")
        return best_move

    return None  # Không thể tối ưu vùng sống


def predator_move(grid, self_pos, opponent_pos):
    """
    Heuristic A* cho Predator.

    Chiến lược:
      1. Grey kề cạnh → bắt ngay.
      2. Tối ưu được vùng sống Grey (AP hoặc Shrink) → dùng chiến lược đó.
      3. Không tối ưu được → A* mặc định đuổi thẳng Grey (đường chim bay).

    Args:
        grid:         bản đồ game (2D list)
        self_pos:     vị trí Predator hiện tại (tuple)
        opponent_pos: vị trí Grey hiện tại (tuple)

    Returns:
        tuple (x, y) — vị trí Predator sẽ di chuyển đến
    """
    pred_pos = self_pos
    grey_pos = opponent_pos

    px, py = pred_pos
    valid_moves = [
        (px + dx, py + dy)
        for dx, dy in DIRECTIONS
        if is_valid((px + dx, py + dy), grid)
    ]
    if not valid_moves:
        return pred_pos

    # Ưu tiên 1: Grey kề cạnh → bắt ngay
    if grey_pos in valid_moves:
        print(f"[Predator] CATCH | pos={pred_pos} -> grey={grey_pos}")
        return grey_pos

    # Ưu tiên 2: Tối ưu được vùng sống → dùng chiến lược AP / Shrink
    optimize_move = _get_optimize_move(grid, pred_pos, grey_pos, valid_moves)
    if optimize_move is not None:
        return optimize_move

    # Ưu tiên 3: Không tối ưu được → A* mặc định (đường chim bay)
    astar_move = astar_next_step(grid, pred_pos, grey_pos)
    if astar_move != pred_pos:
        print(f"[Predator] FALLBACK A* | pos={pred_pos} -> move={astar_move}")
        return astar_move

    return valid_moves[0]