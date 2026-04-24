import heapq

class PredatorAStar:
    name = "A*"

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

        # A* algorithm
        open_set = []
        heapq.heappush(open_set, (0, pos))  # (f, position)
        came_from = {}
        g_score = {pos: 0}
        f_score = {pos: self._heuristic(pos, target)}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == target:
                break

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and
                    game_map[neighbor[0]][neighbor[1]] != simulator.grid.WALL):

                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, target)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        if target not in came_from:
            return None

        # truy vết
        path = []
        cur = target
        while cur in came_from:
            path.append(cur)
            cur = came_from[cur]

        path.reverse()

        if len(path) > 0:
            return path[0]  # trả về bước đầu tiên từ vị trí hiện tại
        else:
            return None

    def _heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_distance(start, target, game_map, WALL):
    import heapq
    start = tuple(start)
    target = tuple(target)
    
    rows = len(game_map)
    cols = len(game_map[0])
    
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target:
            return g_score[current]
            
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if (0 <= nx < rows and 0 <= ny < cols and game_map[nx][ny] != WALL):
                tentative_g_score = g_score[current] + 1
                if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g_score
                    f_score = tentative_g_score + heuristic((nx, ny), target)
                    heapq.heappush(open_set, (f_score, (nx, ny)))
    return -1

class PreyAStar:
    name = "A*"

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

            if (0 <= nx < rows and 0 <= ny < cols and game_map[nx][ny] != WALL):
                dist = astar_distance((nx, ny), predator, game_map, WALL)

                if dist > max_distance:
                    max_distance = dist
                    best_move = (nx, ny)

        return best_move