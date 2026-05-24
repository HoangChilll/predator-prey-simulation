import heapq
from ui.constants import DIRECTIONS, is_valid



def heuristic(a, b):
    """
    Manhattan distance.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])




def predatorgreedy(grid, self_pos, opponent_pos):
    """
    Greedy Best-First Search cho con đi săn.


    Input:
    - grid: object có rows, cols, cells
    - self_pos: vị trí con đi săn
    - opponent_pos: vị trí con bị săn


    Output:
    - vị trí tiếp theo của con đi săn
    """


    start = tuple(self_pos)
    goal = tuple(opponent_pos)


    open_list = []
    counter = 0


    # Priority queue ưu tiên ô có h(n) nhỏ nhất
    heapq.heappush(open_list, (heuristic(start, goal), counter, start))


    # parent dùng để truy vết đường đi
    parent = {start: None}


    while open_list:
        _, _, current = heapq.heappop(open_list)


        if current == goal:
            break


        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)


            if is_valid(grid, neighbor) and neighbor not in parent:
                parent[neighbor] = current


                counter += 1
                heapq.heappush(
                    open_list,
                    (heuristic(neighbor, goal), counter, neighbor)
                )


    # Nếu không tìm được đường thì đứng yên
    if goal not in parent:
        return start


    # Truy vết path từ goal về start
    path = []
    cur = goal


    while cur is not None:
        path.append(cur)
        cur = parent[cur]


    path.reverse()


    # path[0] là current, path[1] là bước tiếp theo
    if len(path) < 2:
        return start


    return path[1]





def preygreedy(grid, self_pos, opponent_pos):
    """
    Greedy cho Prey.


    Input chuẩn:
    - grid: ma trận bản đồ
    - self_pos: vị trí hiện tại của prey
    - opponent_pos: vị trí predator


    Ý tưởng:
    - Prey chọn ô làm khoảng cách tới predator lớn nhất.
    """


    start = tuple(self_pos)
    predator = tuple(opponent_pos)


    best_move = start
    max_distance = -1


    for dx, dy in DIRECTIONS:
        candidate = (start[0] + dx, start[1] + dy)

        if is_valid(grid, candidate):
            dist = heuristic(candidate, predator)


            # Chọn ô xa predator nhất
            if dist > max_distance:
                max_distance = dist
                best_move = candidate


    return best_move


# tí nx tôi commit cái này lên, thì ô switch sang nhánh ui rồi chạy trên đấy, đừng push lên, sửa gì thì bảo tôi, 