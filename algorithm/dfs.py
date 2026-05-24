from ui.constants import DIRECTIONS, is_valid


def heuristic(a, b):
    """
    Hàm heuristic dùng Manhattan distance.
    (Giữ lại để dùng cho logic chạy trốn của Prey)


    Input:
    - a: tọa độ (x1, y1)
    - b: tọa độ (x2, y2)


    Output:
    - khoảng cách ước lượng từ a đến b
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])




def predator_dfs_move(grid, self_pos, opponent_pos):
    """
    Thuật toán Depth-First Search (DFS).


    Input chuẩn:
    - grid: ma trận bản đồ
    - self_pos: vị trí hiện tại của agent, dạng (x, y)
    - opponent_pos: vị trí đối thủ, dạng (x, y)


    Output:
    - vị trí tiếp theo agent sẽ đi, dạng (x, y)
    """


    # Ép về tuple để dùng làm key trong dict/set
    start = tuple(self_pos)
    goal = tuple(opponent_pos)


    # Stack: lưu trữ theo cấu trúc (vị_trí_hiện_tại, đường_đi_đến_vị_trí_này)
    # LIFO: node đưa vào sau cùng sẽ được lấy ra trước
    stack = [(start, [start])]
    visited = set()


    while stack:
        # Lấy node ở đỉnh Stack
        current, path = stack.pop()


        # Bỏ qua nếu đã duyệt qua ô này
        if current in visited:
            continue
           
        # Đánh dấu đã thăm
        visited.add(current)


        # Nếu tới đích thì dừng
        if current == goal:
            # Nếu có đường đi, trả về bước đầu tiên (sau start)
            if len(path) > 1:
                return path[1]
            return start


        x, y = current


        # Duyệt 4 ô lân cận
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)


            # Chỉ xét ô hợp lệ và chưa đi qua
            if is_valid(neighbor, grid) and neighbor not in visited:
                # Cập nhật đường đi mới và đưa vào Stack
                stack.append((neighbor, path + [neighbor]))


    # Nếu không tìm được đường thì đứng yên
    return start




def prey_dfs_move(grid, self_pos, opponent_pos):
    """
    Logic di chuyển cho Prey.


    Input chuẩn:
    - grid: ma trận bản đồ
    - self_pos: vị trí hiện tại của prey
    - opponent_pos: vị trí predator


    Ý tưởng:
    - Prey vẫn ưu tiên chọn ô làm khoảng cách tới predator lớn nhất để sống sót.
    """


    start = tuple(self_pos)
    predator = tuple(opponent_pos)


    best_move = start
    max_distance = -1


    for dx, dy in DIRECTIONS:
        candidate = (start[0] + dx, start[1] + dy)

        if is_valid(candidate, grid):
            dist = heuristic(candidate, predator)


            # Chọn ô xa predator nhất
            if dist > max_distance:
                max_distance = dist
                best_move = candidate


    return best_move




