from collections import deque

class PredatorBFS:
    name = "BFS"

    def get_move(self, pos, simulator, targets):
        if not targets:
            return None
        
        pos = tuple(pos)
        targets = [tuple(t) for t in targets]

        target = targets[0]  # đuổi con đầu tiên
        game_map = simulator.grid.cells

        rows = len(game_map)
        cols = len(game_map[0])

        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        queue = deque([pos])
        parent = {pos: None}

        while queue:
            current = queue.popleft()

            if current == target:
                break

            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy

                if (0 <= nx < rows and 0 <= ny < cols and
                    game_map[nx][ny] != simulator.grid.WALL and
                    (nx, ny) not in parent):

                    queue.append((nx, ny))
                    parent[(nx, ny)] = current

        if target not in parent:
            return None

        # truy vết
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = parent[cur]

        path.reverse()

        if len(path) < 2:
            return None

        return path[1]  #  trả về tọa độ luôn

def bfs_distance(start, target, game_map, WALL):

    start = tuple(start)     #  FIX
    target = tuple(target)   #  FIX

    rows = len(game_map)
    cols = len(game_map[0])

    queue = deque([start])
    visited = {start: 0}

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:
        current = queue.popleft()
        x, y = current
        
        if (x, y) == target:
            return visited[(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (0 <= nx < rows and 0 <= ny < cols and
                game_map[nx][ny] != WALL and
                (nx, ny) not in visited):

                visited[(nx, ny)] = visited[(x, y)] + 1
                queue.append((nx, ny))

    return -1

class PreyBFS:
    name = "BFS"

    def get_move(self, pos, simulator, targets):
        if not targets:
            return None

        predator = targets[0]
        game_map = simulator.grid.cells
        WALL = simulator.grid.WALL

        rows = len(game_map)
        cols = len(game_map[0])

        directions = [
            (-1,0), (1,0), (0,-1), (0,1),
            (0,0)  # đứng yên
        ]

        best_move = None
        max_distance = -1

        for dx, dy in directions:
            nx, ny = pos[0] + dx, pos[1] + dy

            if (0 <= nx < rows and 0 <= ny < cols and
                game_map[nx][ny] != WALL):

                dist = bfs_distance(
                    (nx, ny),
                    predator,
                    game_map,
                    WALL
                )

                if dist > max_distance:
                    max_distance = dist
                    best_move = (nx, ny)

        return best_move