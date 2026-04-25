class DFSStrategy:
    def __init__(self):
        # Biến lưu số lượng node đã mở rộng để phục vụ thống kê, so sánh
        self.nodes_expanded = 0

    def get_action(self, state):
        """
        Duyệt đồ thị bằng thuật toán Depth-First Search (Graph Search).
        Trả về action (d_row, d_col) cho bước đi tiếp theo.
        """
        # Ép kiểu tọa độ về dạng tuple để có thể hash và đưa vào Set
        start = tuple(state.predator_pos)
        goal = tuple(state.grey_pos)

        # Stack chứa các tuple: (vị_trí_hiện_tại, danh_sách_các_hành_động_để_đến_đây)
        stack = [(start, [])]
        
        # Set lưu các tọa độ đã duyệt để tránh vòng lặp vô hạn
        visited = set()
        
        # Reset biến log trước mỗi lượt (turn)
        self.nodes_expanded = 0

        # Các hướng di chuyển: Lên, Xuống, Trái, Phải
        # Đặc thù của DFS (Stack): Hướng được thêm vào cuối cùng sẽ được duyệt đầu tiên.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            current_pos, path = stack.pop()

            # Bỏ qua nếu node này đã được xử lý
            if current_pos in visited:
                continue
                
            # Đánh dấu đã duyệt và tăng biến đếm log
            visited.add(current_pos)
            self.nodes_expanded += 1

            # Kiểm tra trạng thái đích
            if current_pos == goal:
                if path:
                    # Chỉ trả về bước đi ĐẦU TIÊN để agent dịch chuyển 1 ô trên UI
                    return path[0]  
                return (0, 0) # Nếu đã đứng trùng ô với mục tiêu

            r, c = current_pos
            
            # Mở rộng các ô lân cận (Successors)
            for dr, dc in directions:
                next_pos = (r + dr, c + dc)

                # Nếu ô tiếp theo đi được và chưa từng duyệt qua
                if self.is_valid_move(next_pos, state) and next_pos not in visited:
                    # Nối thêm hành động mới vào hành trình hiện tại
                    new_path = path + [(dr, dc)]
                    stack.append((next_pos, new_path))
        
        # Trường hợp bị kẹt (xung quanh toàn tường) không tìm thấy đường
        return (0, 0)

    def is_valid_move(self, pos, state):
        """
        Kiểm tra tính hợp lệ của ô lưới tiếp theo.
        """
        r, c = pos
        
        # 1. Không vượt quá ranh giới bản đồ
        if r < 0 or r >= state.rows or c < 0 or c >= state.cols:
            return False
            
        # 2. Không đi xuyên tường (Nếu state có định nghĩa tường)
        if hasattr(state, 'is_wall') and state.is_wall(r, c):
            return False
            
        return True