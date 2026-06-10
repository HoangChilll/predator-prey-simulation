from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited

def heuristic(a, b):
    
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def predator_dfs_move(grid, self_pos, opponent_pos):
    

    # Ép về tuple để dùng làm key trong dict/set
    start = tuple(self_pos)
    goal = tuple(opponent_pos)


    # Stack: lưu trữ theo cấu trúc (vị_trí_hiện_tại, đường_đi_đến_vị_trí_này)
    # LIFO: node đưa vào sau cùng sẽ được lấy ra trước
    stack = [(start, [start])]
    visited = set()
    visited_order = []   # Thứ tự duyệt để visualize


    while stack:
        # Lấy node ở đỉnh Stack
        current, path = stack.pop()


        # Bỏ qua nếu đã duyệt qua ô này
        if current in visited:
            continue
           
        # Đánh dấu đã thăm
        visited.add(current)
        visited_order.append(current)


        # Nếu tới đích thì dừng
        if current == goal:
            # Ghi visited để visualize
            set_visited(visited_order, path)
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
    set_visited(visited_order, [])
    return start




