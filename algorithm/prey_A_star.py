
import heapq
from collections import deque
from ui.constants import DIRECTIONS, is_valid
 
def flood_fill(grid, start, blocked=None):
    """
    BFS lan ra từ start, đếm tất cả ô có thể đến được.
    Dùng để đo "không gian sống" của Prey tại mỗi nước đi.
    """
    if blocked is None:
        blocked = set()
 
    visited = {start}
    queue   = deque([start])
 
    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in visited and nxt not in blocked and is_valid(nxt, grid):
                visited.add(nxt)
                queue.append(nxt)
 
    return visited
 
 
def find_articulation_points(grid, start, blocked=None):
    """
    Tìm articulation points (điểm thắt cổ chai) trong vùng Prey có thể đến.
    Dùng Tarjan iterative để tránh RecursionError trên map lớn.
 
    AP = ô mà nếu đi qua đó, Prey có thể bị nhốt vào vùng nhỏ hơn.
    Prey nên TRÁNH đi qua các AP này trừ khi vùng phía sau đủ rộng.
    """
    if blocked is None:
        blocked = set()
 
    reachable = flood_fill(grid, start, blocked)
    if not reachable:
        return set()
 
    visited = {}
    low     = {}
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
 
 
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
 
 
# ============================================================
# Hàm phụ riêng cho Prey
# ============================================================

def component_size_after_crossing(grid, crossing_pos, from_pos, blocked=None):
    """
    Nếu Prey bước từ from_pos sang crossing_pos (một AP),
    vùng phía sau crossing_pos có bao nhiêu ô?

    Dùng để quyết định: "Ngõ kia tuy là AP nhưng vẫn rộng không?"

    Args:
        crossing_pos: ô AP Prey cân nhắc bước vào
        from_pos:     vị trí Prey hiện tại (để không flood ngược lại)

    Returns:
        int — số ô phía sau AP
    """
    if blocked is None:
        blocked = set()

    # Coi from_pos là blocked để flood fill chỉ đếm vùng PHÍA TRƯỚC
    blocked_sim = blocked | {from_pos}
    component = flood_fill(grid, crossing_pos, blocked=blocked_sim)
    return len(component)
 
 
def voronoi_prey_area(grid, prey_pos, pred_pos):
    """
    Tính "lãnh thổ Voronoi" của Prey:
    Số ô mà Prey đến được TRƯỚC Predator (BFS song song từ cả hai).

    Càng nhiều ô Prey sở hữu → Prey càng an toàn.

    Returns:
        int — số ô thuộc lãnh thổ Prey
    """
    prey_territory = set()
    visited        = {}  # pos -> người đến trước ('prey' hoặc 'pred')

    # BFS song song: Prey và Predator cùng xuất phát
    queue = deque()
    queue.append(('prey', prey_pos, 0))
    queue.append(('pred', pred_pos, 0))
    visited[prey_pos] = 'prey'
    visited[pred_pos] = 'pred'

    while queue:
        owner, (x, y), dist = queue.popleft()
        if owner == 'prey':
            prey_territory.add((x, y))

        for dx, dy in DIRECTIONS:
            nxt = (x + dx, y + dy)
            if nxt not in visited and is_valid(nxt, grid):
                visited[nxt] = owner
                queue.append((owner, nxt, dist + 1))

    return len(prey_territory)
 
# ============================================================
# Hàm chính — Prey Move
# ============================================================
 
def prey_move(grid, self_pos, opponent_pos):
    """
    Heuristic A* cho Prey.
 
    Chiến lược (ưu tiên theo thứ tự):
      1. Tránh đi vào ô AP mà phía sau là vùng quá nhỏ
         (ngõ cụt thực sự → không đi dù xa Predator hơn)
      2. Trong các bước đi an toàn → chọn bước nào giữ được
         không gian sống lớn nhất và xa Predator nhất
      3. Nếu mọi bước đều là AP → chọn AP có vùng phía sau lớn nhất
         (buộc phải chọn ít tệ nhất)
 
    Heuristic mỗi bước đi 'move':
        score = - W_AREA     × reachable_area(move)   (tối đa hóa)
                - W_DIST     × dist(move → predator)   (tối đa hóa)
                + W_VORONOI  × voronoi_prey_area(move) (tối đa hóa)
                + W_AP_PEN   × ap_penalty(move)        (phạt nếu là AP nhỏ)
 
    Args:
        grid:         bản đồ game
        self_pos:     vị trí Prey hiện tại (tuple)
        opponent_pos: vị trí Predator hiện tại (tuple)
 
    Returns:
        tuple (x, y) — vị trí Prey sẽ di chuyển đến
    """
    prey_pos = self_pos
    pred_pos = opponent_pos
 
    # Trọng số — có thể chỉnh tuỳ map
    W_AREA    = 0.5   # ưu tiên vùng rộng
    W_DIST    = 0.3   # ưu tiên xa Predator
    W_VORONOI = 0.2   # ưu tiên lãnh thổ Voronoi của Prey
    W_AP_PEN  = 0.8   # phạt nặng nếu bước vào AP dẫn vào vùng nhỏ
 
    # Ngưỡng: nếu vùng sau AP nhỏ hơn ngưỡng này → coi là ngõ cụt thực sự
    DEAD_END_THRESHOLD = 8
 
    # --- Các bước đi hợp lệ ---
    px, py = prey_pos
    valid_moves = [
        (px + dx, py + dy)
        for dx, dy in DIRECTIONS
        if is_valid((px + dx, py + dy), grid)
    ]
    if not valid_moves:
        return prey_pos
 
    # --- Tìm APs tại vị trí hiện tại của Prey ---
    art_points = find_articulation_points(grid, prey_pos, blocked={pred_pos})
 
    # --- Đánh giá từng bước đi ---
    scored_moves = []
 
    for move in valid_moves:
 
        # 1. Đo "không gian sống" nếu đi đến 'move'
        reachable     = flood_fill(grid, move, blocked={pred_pos})
        area          = len(reachable)
 
        # 2. Khoảng cách đến Predator (xa hơn → tốt hơn)
        dist_to_pred  = manhattan(move, pred_pos)
 
        # 3. Voronoi territory của Prey sau khi dời sang 'move'
        voronoi_area  = voronoi_prey_area(grid, move, pred_pos)
 
        # 4. AP penalty
        # Nếu 'move' là một articulation point → kiểm tra vùng phía sau
        ap_penalty = 0.0
        if move in art_points:
            size_behind = component_size_after_crossing(
                grid, move, from_pos=prey_pos, blocked={pred_pos}
            )
            if size_behind < DEAD_END_THRESHOLD:
                # Ngõ cụt thực sự → phạt nặng
                ap_penalty = (DEAD_END_THRESHOLD - size_behind) * 10
            else:
                # AP nhưng vùng sau vẫn rộng → phạt nhẹ
                ap_penalty = 2.0
 
        # 5. Tổng hợp score (score THẤP = tốt hơn)
        score = (
            - W_AREA    * area
            - W_DIST    * dist_to_pred
            - W_VORONOI * voronoi_area
            + W_AP_PEN  * ap_penalty
        )
 
        scored_moves.append((score, move, area, ap_penalty))
        print(f"  [Prey] cân nhắc {move}: area={area}, "
              f"dist_pred={dist_to_pred}, voronoi={voronoi_area}, "
              f"ap_penalty={ap_penalty:.1f} -> score={score:.2f}")
 
    # --- Chọn bước tốt nhất ---
    # Ưu tiên bước không phải ngõ cụt (ap_penalty < ngưỡng nặng)
    safe_moves = [(s, m, a, p) for s, m, a, p in scored_moves if p < 5.0]
 
    if safe_moves:
        # Trong các bước an toàn → chọn score thấp nhất
        best = min(safe_moves, key=lambda x: x[0])
    else:
        # Mọi bước đều nguy hiểm → chọn bước ít tệ nhất (area lớn nhất)
        best = max(scored_moves, key=lambda x: x[2])
        print("[Prey] Moi buoc deu la AP/ngo cut -> chon vung lon nhat")
 
    chosen_move = best[1]
    print(f"[Prey] pos={prey_pos} -> move={chosen_move} | "
          f"area={best[2]} | ap_penalty={best[3]:.1f} | score={best[0]:.2f}")
 
    return tuple(chosen_move)