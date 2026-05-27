import math




def euclid_distance(a, b):
    """
    Tính khoảng cách Euclid giữa 2 điểm.
    Đây là khoảng cách chim bay, không xét tường.
    """
    return (
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    ) ** 0.5








def manhattan_distance(a, b):
    """
    Tính khoảng cách Manhattan giữa 2 điểm.
    Dùng khi di chuyển kiểu grid 4 hướng.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])








def get_neighbors(pos, map_data, include_stay=True):
    """Lấy danh sách các vị trí lân cận hợp lệ."""
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]




    if include_stay:
        directions.append((0, 0))




    # Xác định kích thước bản đồ
    if hasattr(map_data, 'rows'):  # Nếu là đối tượng Grid
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else:  # Nếu là mảng 2D list of lists
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
    """
    Hàm đánh giá: khoảng cách Euclid giữa Predator và Prey.




    Bản của bạn m dùng:
        return bfs_distance(pred_pos, prey_pos, map_data)




    Bản của m dùng Euclid:
        return euclid_distance(pred_pos, prey_pos)
    """
    return euclid_distance(pred_pos, prey_pos)








def minimax(map_data, pred_pos, prey_pos, depth, alpha, beta, is_maximizing):
    """
    Thuật toán Minimax với Alpha-Beta Pruning.




    Prey là người chơi Maximizing:
        muốn tối đa hóa khoảng cách.




    Predator là người chơi Minimizing:
        muốn tối thiểu hóa khoảng cách.
    """
    if pred_pos == prey_pos:
        return -1000  # Predator bắt được Prey




    if depth == 0:
        return evaluate(pred_pos, prey_pos, map_data)




    if is_maximizing:
        # Lượt của Prey Maximizing
        max_eval = -float('inf')




        for move in get_neighbors(prey_pos, map_data, include_stay=True):
            eval_score = minimax(
                map_data,
                pred_pos,
                move,
                depth - 1,
                alpha,
                beta,
                False
            )




            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)




            if beta <= alpha:
                break




        return max_eval




    else:
        # Lượt của Predator Minimizing
        min_eval = float('inf')




        for move in get_neighbors(pred_pos, map_data, include_stay=False):
            eval_score = minimax(
                map_data,
                move,
                prey_pos,
                depth - 1,
                alpha,
                beta,
                True
            )




            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)




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
        eval_score = minimax(
            map_data,
            move,
            prey_pos,
            depth - 1,
            -float('inf'),
            float('inf'),
            True
        )




        if eval_score < best_eval:
            best_eval = eval_score
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
        eval_score = minimax(
            map_data,
            pred_pos,
            move,
            depth - 1,
            -float('inf'),
            float('inf'),
            False
        )




        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move




    return best_move








def prey_minimax_shortest_path(map_data, prey_pos, pred_pos):
    return get_predator_move(map_data, prey_pos, pred_pos, depth=4)




def grey_minimax_shortest_path(map_data, pred_pos, prey_pos):
    return get_prey_move(map_data, prey_pos, pred_pos, depth=4)
