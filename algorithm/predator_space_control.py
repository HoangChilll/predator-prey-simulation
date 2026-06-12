import heapq
from collections import deque
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited
 
 # thuật toán tìm không gian sống của prey
 #start là vị trí xuất phát của prey , blocked là vị trí của predator, prey không được đi vào 
def flood_fill(grid, start, blocked=None):
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
    return visited  # tất cả các ô có thể đi được từ start hay không gian sống
 
# thuật toán tìm Articulation Points (điểm thắt cổ chai) hay điểm mà prey đến được đó thì prey sẽ bị nhốt
# Tham khao thuật toán Tarjan 
def find_articulation_points(grid, start, blocked=None):
    if blocked is None:
        blocked = set()
    # Chỉ xét các ô prey có thể đến được
    reachable = flood_fill(grid, start, blocked)
    if not reachable:
        return set()
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
    return ap #trả về các điểm thắt cổ chai
 
 
# A* mặc định nếu không có điểm thắt cổ chai
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
 
 
def next_step(grid, start, goal, blocked=None):

    if blocked is None:
        blocked = set()
 
    if start == goal:
        return start
 
    # (f_score, g_score, vị_trí)
    open_heap = [(manhattan(start, goal), 0, start)]
    g_score   = {start: 0}
    came_from = {}
    visited_order = []   # Thứ tự duyệt để visualize
 
    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        visited_order.append(current)
 
        if current == goal:
            # Truy vết path để gửi visualize
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            set_visited(visited_order, path)
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
 
    set_visited(visited_order, [])
    return start  # Không tìm được đường
 
 
#A* cho prey
def _bfs_dist(grid, start, goal):
    #BFS distance từ start đến goal
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

#
def optimize_move(grid, pred_pos, prey_pos, valid_moves):

    reachable = flood_fill(grid, prey_pos, blocked={pred_pos})
    art_points = find_articulation_points(grid, prey_pos, blocked={pred_pos})

    # AP tìm đến điểm thắt cổ chai
    valuable_aps = [
        ap for ap in art_points
        if _bfs_dist(grid, pred_pos, ap) <= _bfs_dist(grid, prey_pos, ap)
    ]

    if valuable_aps:
        best_ap = min(valuable_aps, key=lambda ap: _bfs_dist(grid, prey_pos, ap))
        ap_move = next_step(grid, pred_pos, best_ap)
        if ap_move != pred_pos:
            # Chỉ dùng AP nếu bước đó không làm predator xa prey hơn
            if _bfs_dist(grid, ap_move, prey_pos) <= _bfs_dist(grid, pred_pos, prey_pos):
                set_visited(list(reachable), [pred_pos, ap_move], overlay=reachable, art_points=art_points)
                return ap_move

    # Shrink tìm đến điểm làm giảm không gian sống của prey
    current_prey_area = len(reachable)
    best_move = None
    best_reduction = 0
    visited_order = [pred_pos]

    for move in valid_moves:
        new_prey_area = len(flood_fill(grid, prey_pos, blocked={move}))
        reduction = current_prey_area - new_prey_area
        visited_order.append(move)
        if reduction > best_reduction:
            best_reduction = reduction
            best_move = move

    if best_move is not None:
        # Chỉ dùng Shrink nếu bước đó không làm predator xa prey hơn
        if _bfs_dist(grid, best_move, prey_pos) <= _bfs_dist(grid, pred_pos, prey_pos):
            set_visited(list(reachable), [pred_pos, best_move], overlay=reachable, art_points=art_points)
            return best_move

    return None  # Không thể tối ưu 

#  nếu tối ưu được vùng sống thì dùng không được thì dùng A* mặc định
def predator_space_control(grid, self_pos, opponent_pos):
    pred_pos = self_pos
    prey_pos = opponent_pos

    px, py = pred_pos
    valid_moves = [
        (px + dx, py + dy)
        for dx, dy in DIRECTIONS
        if is_valid((px + dx, py + dy), grid)
    ]
    if not valid_moves:
        return pred_pos

    #  Prey kề cạnh → bắt ngay
    if prey_pos in valid_moves:
        set_visited([pred_pos, prey_pos], [pred_pos, prey_pos])
        return prey_pos

    #  Tối ưu được vùng sống dùng chiến lược AP / Shrink
    optimize_move1 = optimize_move(grid, pred_pos, prey_pos, valid_moves)
    if optimize_move1 is not None:
        return optimize_move1

    # Không tối ưu được dùng A* mặc định 
    astar_move1 = next_step(grid, pred_pos, prey_pos)
    if astar_move1 != pred_pos:
        return astar_move1

    return valid_moves[0]