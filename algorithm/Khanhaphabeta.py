from collections import deque


def dfs_distance(start, target, map_data):
    """Tính khoảng cách bằng DFS giữa hai điểm trên bản đồ (Đường đi tìm thấy đầu tiên)."""
    if start == target:
        return 0
   
    # Xác định kích thước bản đồ và cách kiểm tra tường
    if hasattr(map_data, 'rows'):
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else:
        rows, cols = len(map_data), len(map_data[0])
        is_wall = lambda r, c: map_data[r][c] == 1


    # Sử dụng list như một Stack (LIFO) cho DFS
    stack = [(start, 0)]
    visited = {start}
   
    while stack:
        (curr_x, curr_y), dist = stack.pop() # LẤY ĐUÔI 	       
        # Thử 4 hướng di chuyển
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
           
            if (nx, ny) == target:
                return dist + 1
           
            if (0 <= nx < rows and 0 <= ny < cols and
                not is_wall(nx, ny) and
                (nx, ny) not in visited):
               
                visited.add((nx, ny))
                stack.append(((nx, ny), dist + 1))
   
    return 100 # Không tìm thấy đường đi


def get_neighbors(pos, map_data, include_stay=True):
    """Lấy danh sách các vị trí lân cận hợp lệ."""
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if include_stay:
        directions.append((0, 0))
       
    if hasattr(map_data, 'rows'):
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else:
        rows, cols = len(map_data), len(map_data[0])
        is_wall = lambda r, c: map_data[r][c] == 1


    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if not is_wall(nx, ny):
                neighbors.append((nx, ny))
    return neighbors


def evaluate(pred_pos, prey_pos, map_data):
    """Hàm đánh giá: khoảng cách DFS giữa Predator và Prey."""
    return dfs_distance(pred_pos, prey_pos, map_data)


def minimax(map_data, pred_pos, prey_pos, depth, alpha, beta, is_maximizing):
    if pred_pos == prey_pos:
        return -1000
   
    if depth == 0:
        return evaluate(pred_pos, prey_pos, map_data)


    if is_maximizing:
        max_eval = -float('inf')
        for move in get_neighbors(prey_pos, map_data, include_stay=True):
            eval_val = minimax(map_data, pred_pos, move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_val)
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_neighbors(pred_pos, map_data, include_stay=False):
            eval_val = minimax(map_data, move, prey_pos, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_val)
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        return min_eval


def get_predator_move(map_data, pred_pos, prey_pos, depth=2):
    best_eval = float('inf')
    best_move = pred_pos
    for move in get_neighbors(pred_pos, map_data, include_stay=False):
        eval_val = minimax(map_data, move, prey_pos, depth - 1, -float('inf'), float('inf'), True)
        if eval_val < best_eval:
            best_eval = eval_val
            best_move = move
    return best_move


def get_prey_move(map_data, pred_pos, prey_pos, depth=2):
    best_eval = -float('inf')
    best_move = prey_pos
    for move in get_neighbors(prey_pos, map_data, include_stay=True):
        eval_val = minimax(map_data, pred_pos, move, depth - 1, -float('inf'), float('inf'), False)
        if eval_val > best_eval:
            best_eval = eval_val
            best_move = move
    return best_move


def predator_minimax_shortest_path(map_data, pred_pos, prey_pos):
    return get_predator_move(map_data, pred_pos, prey_pos, depth=4)


def prey_minimax_shortest_path(map_data, prey_pos, pred_pos):
    return get_prey_move(map_data, pred_pos, prey_pos, depth=4)


