import random
from collections import deque


def _bfs_path_exists(maze, start, goal):
    n = len(maze)
    visited = {start}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return False


def generate_random_maze(n):
    """Tạo mê cung ngẫu nhiên n×n đảm bảo có đường từ (0,0) đến (10,10).

    - Tường (1): 40-60% tổng ô.
    - Start = (0,0), Goal = (10,10).
    - n phải > 10 (để ô (10,10) tồn tại).
    """
    if n <= 10:
        raise ValueError(f"n phải > 10 để tồn tại ô (10,10), nhận được n={n}")

    total = n * n
    min_walls = int(total * 0.4)
    max_walls = int(total * 0.6)

    for _ in range(200):
        # Bước 1: Tạo đường đi ngẫu nhiên từ (0,0) đến (10,10)
        # Dùng đúng 10 bước xuống + 10 bước phải, xáo trộn thứ tự
        moves = [(1, 0)] * 10 + [(0, 1)] * 10
        random.shuffle(moves)

        path_cells = set()
        r, c = 0, 0
        path_cells.add((r, c))
        for dr, dc in moves:
            r, c = r + dr, c + dc
            path_cells.add((r, c))

        # Bước 2: Với các ô còn lại, phân bổ tường để đạt tỉ lệ 40-60%
        remaining = [(i, j) for i in range(n) for j in range(n) if (i, j) not in path_cells]
        random.shuffle(remaining)

        target_walls = random.randint(min_walls, max_walls)
        walls_to_place = min(target_walls, len(remaining))
        wall_set = set(remaining[:walls_to_place])

        maze = [
            [1 if (i, j) in wall_set else 0 for j in range(n)]
            for i in range(n)
        ]

        # Bước 3: Kiểm tra BFS và tỉ lệ tường
        if not _bfs_path_exists(maze, (0, 0), (10, 10)):
            continue
        actual_walls = sum(maze[i][j] for i in range(n) for j in range(n))
        if min_walls <= actual_walls <= max_walls:
            return maze

    # Fallback: đường L-shape đơn giản nếu vẫn không thỏa sau 200 lần
    maze = [[1] * n for _ in range(n)]
    for col in range(11):
        maze[0][col] = 0
    for row in range(1, 11):
        maze[row][10] = 0
    return maze
