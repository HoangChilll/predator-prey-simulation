# Dữ liệu ghi bởi thuật toán 
_all_visited: list = []
_all_path: list = []
_all_scores: dict = {}
_all_overlay: set = set()
_all_art_points: set = set()

#  Dữ liệu hiển thị
_display_visited: list = []
_display_path: list = []
_display_scores: dict = {}
_display_overlay: set = set()
_display_art_points: set = set()


def set_visited(cells: list, path: list = None, scores: dict = None,
                overlay: list = None, art_points: list = None):
    
    global _all_visited, _all_path, _all_scores, _all_overlay, _all_art_points
    _all_visited = list(cells)
    _all_path = list(path) if path else []
    _all_scores = dict(scores) if scores else {}
    _all_overlay = set(overlay) if overlay else set()
    _all_art_points = set(art_points) if art_points else set()


def get_all():
    #Trả về (all_visited, all_path) 
    return _all_visited, _all_path


def set_display(cells: list, path: list = None, scores: dict = None,
                overlay: list = None, art_points: list = None):
   
    global _display_visited, _display_path, _display_scores, _display_overlay, _display_art_points
    _display_visited = list(cells)
    _display_path = list(path) if path else []
    if scores is None:
        _display_scores = {pos: _all_scores[pos] for pos in cells if pos in _all_scores}
    else:
        _display_scores = dict(scores)
    _display_overlay = set(overlay) if overlay is not None else set(_all_overlay)
    _display_art_points = set(art_points) if art_points is not None else set(_all_art_points)


def get_display():
    
    return (_display_visited, _display_path,
            _display_scores, _display_overlay, _display_art_points)


def clear():
    #Xóa toàn bộ dữ liệu
    global _all_visited, _all_path, _all_scores, _all_overlay, _all_art_points
    global _display_visited, _display_path, _display_scores, _display_overlay, _display_art_points
    _all_visited = []
    _all_path = []
    _all_scores = {}
    _all_overlay = set()
    _all_art_points = set()
    _display_visited = []
    _display_path = []
    _display_scores = {}
    _display_overlay = set()
    _display_art_points = set()
