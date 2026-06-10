import heapq
from ui.constants import DIRECTIONS, is_valid
from algorithm.visited_tracker import set_visited



def heuristic(a, b):
    """
    Manhattan distance.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])




def predator_greedy(grid, self_pos, opponent_pos):



    start = tuple(self_pos)
    goal = tuple(opponent_pos)


    open_list = []
    counter = 0
    visited_order = []   # Thứ tự duyệt để visualize


    # Priority queue ưu tiên ô có h(n) nhỏ nhất
    heapq.heappush(open_list, (heuristic(start, goal), counter, start))


    # parent dùng để truy vết đường đi
    parent = {start: None}


    while open_list:
        _, _, current = heapq.heappop(open_list)
        visited_order.append(current)


        if current == goal:
            break


        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)


            if is_valid(neighbor, grid) and neighbor not in parent:
                parent[neighbor] = current


                counter += 1
                heapq.heappush(
                    open_list,
                    (heuristic(neighbor, goal), counter, neighbor)
                )


    # Nếu không tìm được đường thì đứng yên
    if goal not in parent:
        set_visited(visited_order, [])
        return start


    # Truy vết path từ goal về start
    path = []
    cur = goal


    while cur is not None:
        path.append(cur)
        cur = parent[cur]


    path.reverse()

    # Ghi visited để visualize
    set_visited(visited_order, path)

    # path[0] là current, path[1] là bước tiếp theo
    if len(path) < 2:
        return start


    return path[1]





def prey_greedy(grid, self_pos, opponent_pos):


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
 