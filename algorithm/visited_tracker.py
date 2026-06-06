"""
visited_tracker.py
------------------
Module dùng chung để:
  - Thuật toán ghi lại toàn bộ thứ tự duyệt (_all_visited) và path (_all_path)
  - main.py điều khiển animation từng ô một (_display_visited, _display_path)
  - draw_grid đọc từ get_display() để vẽ

Cách dùng trong thuật toán:
    set_visited(visited_order_list, path_list)

Cách dùng trong main.py:
    all_v, all_p = get_all()          # lấy toàn bộ kết quả sau khi algo chạy
    set_display(cells[:i], path)      # cập nhật animation đến ô thứ i
    visited, path = get_display()     # draw_grid gọi cái này
"""

# --- Dữ liệu ghi bởi thuật toán (full traversal order) ---
_all_visited: list = []
_all_path: list = []
_all_scores: dict = {}

# --- Dữ liệu hiển thị (được main.py điều khiển từng ô) ---
_display_visited: list = []
_display_path: list = []
_display_scores: dict = {}


def set_visited(cells: list, path: list = None, scores: dict = None):
    """
    Gọi bởi thuật toán để lưu thứ tự duyệt đầy đủ.
    cells: [(row, col), ...] theo thứ tự duyệt
    path:  [(row, col), ...] đường đi tìm được (nếu có)
    scores: {pos: score} để hiển thị điểm của các nước đi.
    """
    global _all_visited, _all_path, _all_scores
    _all_visited = list(cells)
    _all_path = list(path) if path else []
    _all_scores = dict(scores) if scores else {}


def get_all():
    """Trả về (all_visited, all_path) — toàn bộ kết quả từ thuật toán."""
    return _all_visited, _all_path


def set_display(cells: list, path: list = None, scores: dict = None):
    """
    Gọi bởi main.py để cập nhật những ô đang hiển thị animation.
    cells: subset của _all_visited (đến ô thứ i)
    path:  hiển thị path khi animation hoàn thành
    scores: metadata score cho các ô đang hiển thị
    """
    global _display_visited, _display_path, _display_scores
    _display_visited = list(cells)
    _display_path = list(path) if path else []
    if scores is None:
        _display_scores = {pos: _all_scores[pos] for pos in cells if pos in _all_scores}
    else:
        _display_scores = dict(scores)


def get_display():
    """
    Gọi bởi draw_grid để biết cần vẽ gì.
    Trả về (display_visited, display_path).
    """
    return _display_visited, _display_path, _display_scores


def clear():
    """Xóa toàn bộ dữ liệu."""
    global _all_visited, _all_path, _all_scores, _display_visited, _display_path, _display_scores
    _all_visited = []
    _all_path = []
    _all_scores = {}
    _display_visited = []
    _display_path = []
    _display_scores = {}
