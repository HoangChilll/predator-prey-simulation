from collections import deque

def bfs_distance(start, target, map_data):
    """Tính khoảng cách ngắn nhất bằng BFS giữa hai điểm trên bản đồ."""
    if start == target:
        return 0
    
    # Xác định kích thước bản đồ và cách kiểm tra tường
    if hasattr(map_data, 'rows'):
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else:
        rows, cols = len(map_data), len(map_data[0])
        is_wall = lambda r, c: map_data[r][c] == 1

    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        (curr_x, curr_y), dist = queue.popleft()
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            if (nx, ny) == target:
                return dist + 1
            
            if (0 <= nx < rows and 0 <= ny < cols and
                not is_wall(nx, ny) and 
                (nx, ny) not in visited):
                
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    
    return 100 # Không tìm thấy đường đi

def get_neighbors(pos, map_data, include_stay=True):
    """Lấy danh sách các vị trí lân cận hợp lệ."""
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if include_stay:
        directions.append((0, 0))
        
    # Xác định kích thước bản đồ
    if hasattr(map_data, 'rows'): # Nếu là đối tượng Grid
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else: # Nếu là mảng 2D (list of lists)
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
    """Hàm đánh giá: khoảng cách BFS giữa Predator và Prey."""
    return bfs_distance(pred_pos, prey_pos, map_data)

def minimax(map_data, pred_pos, prey_pos, depth, alpha, beta, is_maximizing):
    """
    Thuật toán Minimax với Alpha-Beta Pruning.
    Prey là người chơi Maximizing (muốn tối đa hóa khoảng cách).
    Predator là người chơi Minimizing (muốn tối thiểu hóa khoảng cách).
    """
    if pred_pos == prey_pos:
        return -1000 # Predator bắt được Prey
    
    if depth == 0:
        return evaluate(pred_pos, prey_pos, map_data)

    if is_maximizing:
        # Lượt của Prey (Maximizing)
        max_eval = -float('inf')
        for move in get_neighbors(prey_pos, map_data, include_stay=True):
            eval = minimax(map_data, pred_pos, move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # Lượt của Predator (Minimizing)
        min_eval = float('inf')
        for move in get_neighbors(pred_pos, map_data, include_stay=False):
            eval = minimax(map_data, move, prey_pos, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_predator_move(map_data, pred_pos, prey_pos, depth=3):
    """
    Tìm nước đi tối ưu cho Predator.
    Trả về: (nx, ny) là tọa độ nước đi tiếp theo.
    """
    best_eval = float('inf')
    best_move = pred_pos
    
    for move in get_neighbors(pred_pos, map_data, include_stay=False):
        eval = minimax(map_data, move, prey_pos, depth - 1, -float('inf'), float('inf'), True)
        if eval < best_eval:
            best_eval = eval
            best_move = move
            
    return best_move

def get_prey_move(map_data, pred_pos, prey_pos, depth=3):
    """
    Tìm nước đi tối ưu cho Prey.
    Trả về: (nx, ny) là tọa độ nước đi tiếp theo.
    """
    best_eval = -float('inf')
    best_move = prey_pos
    
    for move in get_neighbors(prey_pos, map_data, include_stay=True):
        eval = minimax(map_data, pred_pos, move, depth - 1, -float('inf'), float('inf'), False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def predator_minimax_shortest_path(map_data, pred_pos, prey_pos):
    """Wrapper cho Predator Minimax với 3 tham số đầu vào (depth=4)."""
    return get_predator_move(map_data, pred_pos, prey_pos, depth=4)

def prey_minimax_shortest_path(map_data, prey_pos, pred_pos):
    """Wrapper cho Prey Minimax với 3 tham số đầu vào (depth=4)."""
    return get_prey_move(map_data, pred_pos, prey_pos, depth=4)