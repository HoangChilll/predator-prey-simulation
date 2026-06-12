
import heapq
from collections import deque
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited
 
def flood_fill(grid, start, blocked=None):
    
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
 
 

def component_size_after_crossing(grid, crossing_pos, from_pos, blocked=None):
    
    if blocked is None:
        blocked = set()

    # Coi from_pos là blocked để flood fill chỉ đếm vùng PHÍA TRƯỚC
    blocked_sim = blocked | {from_pos}
    component = flood_fill(grid, crossing_pos, blocked=blocked_sim)
    return len(component)
 
 
def voronoi_prey_area(grid, prey_pos, pred_pos):
    
    prey_territory = set()
    visited        = {}  # pos -> người đến trước 

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
 

 
def prey_space_ap(grid, self_pos, opponent_pos):
    
    prey_pos = self_pos
    pred_pos = opponent_pos
 
    # Trọng số — có thể chỉnh tuỳ map
    W_AREA    = 0.5   # ưu tiên vùng rộng
    W_DIST    = 0.3   # ưu tiên xa Predator
    W_VORONOI = 0.2   # ưu tiên lãnh thổ Voronoi của Prey
    W_AP_PEN  = 0.8   # phạt nặng nếu bước vào AP dẫn vào vùng nhỏ
 
    # nếu vùng sau AP nhỏ hơn ngưỡng này  coi là ngõ cụt thực sự
    DEAD_END_THRESHOLD = 8
 
    #Các bước đi hợp lệ
    px, py = prey_pos
    valid_moves = [
        (px + dx, py + dy)
        for dx, dy in DIRECTIONS
        if is_valid((px + dx, py + dy), grid)
    ]
    if not valid_moves:
        return prey_pos
 
    art_points = find_articulation_points(grid, prey_pos, blocked={pred_pos})

    scored_moves = []
 
    for move in valid_moves:
 
        # 1. Đo không gian sống nếu đi đến move
        reachable     = flood_fill(grid, move, blocked={pred_pos})
        area          = len(reachable)
 
        # 2. Khoảng cách đến Predator 
        dist_to_pred  = manhattan(move, pred_pos)
 
        # 3. Voronoi territory của Prey sau khi dời sang 'move'
        voronoi_area  = voronoi_prey_area(grid, move, pred_pos)
 
        # 4. AP penalty
        # Nếu move là một articulation point → kiểm tra vùng phía sau
        ap_penalty = 0.0
        if move in art_points:
            size_behind = component_size_after_crossing(
                grid, move, from_pos=prey_pos, blocked={pred_pos}
            )
            if size_behind < DEAD_END_THRESHOLD:
                # Ngõ cụt thực sự  phạt nặng
                ap_penalty = (DEAD_END_THRESHOLD - size_behind) * 10
            else:
                # AP nhưng vùng sau vẫn rộng  phạt nhẹ
                ap_penalty = 2.0
 
        # 5. Tổng hợp score
        score = (
            - W_AREA    * area
            - W_DIST    * dist_to_pred
            - W_VORONOI * voronoi_area
            + W_AP_PEN  * ap_penalty
        )
 
        scored_moves.append((score, move, area, ap_penalty))
 
    # Chọn bước tốt nhất
    # Ưu tiên bước không phải ngõ cụt
    safe_moves = [(s, m, a, p) for s, m, a, p in scored_moves if p < 5.0]
 
    if safe_moves:
        # Trong các bước an toàn chọn score thấp nhất
        best = min(safe_moves, key=lambda x: x[0])
    else:
        # Mọi bước đều nguy hiểm chọn bước ít tệ nhất
        best = max(scored_moves, key=lambda x: x[2])
 
    chosen_move = best[1]
    # Ghi visited các bước đi được cân nhắc + vị trí hiện tại
    visited_cells = [prey_pos] + valid_moves
    set_visited(visited_cells, [prey_pos, chosen_move])

    return tuple(chosen_move)