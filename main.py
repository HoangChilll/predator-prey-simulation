import pygame
from ui.map import  draw_grid, draw_agents, draw_sim_ui, draw_game_over, font, title_font, btn_rect, buttons, dropdowns
from ui.stage1 import draw_menu
from ui.constants import WIDTH, HEIGHT, log
from ui.stage2 import get_config, draw_config, handle_config_click, handle_config_key, selectMatrix
from ui.button import pause_btn, end_btn
from algorithm.selectalgorithm import selectAlgorithm
from algorithm.dynamic_obstacles import DynamicObstacleManager
import algorithm.visited_tracker as tracker

# STAGE
STATE_MENU   = 1
STATE_CONFIG = 2
STATE_SIM    = 3

config = get_config()
state  = STATE_MENU

# INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

# Các tham số ban đầu
sim = None  #trạng thái
grid = None
dyn_manager = None  # bạt vật cản động

step_delay = 1000
last_step  = pygame.time.get_ticks()

# ── Tham số visualization (đổi màu từng ô theo thời gian thực) ──────────
VIS_CELL_DELAY = 35   # ms mỗi ô khi đang duyệt (35ms ≈ mắt thấy rõ)
VIS_CELL_DELAY_SLOW = 120
VIS_HOLD_AFTER = 500  # ms giữ visited trước khi bắt đầu draw path
VIS_HOLD_AFTER_SLOW = 900
VIS_PATH_DISPLAY = 300  # ms hiển thị đường path trước khi apply move
VIS_PATH_DISPLAY_SLOW = 650

# Trạng thái animation
vis = {
    "active":    False,  # đang trong phase visualize hay không
    "cells":     [],     # toàn bộ danh sách ô đã duyệt (từ thuật toán)
    "path":      [],     # đường đi tìm được
    "idx":       0,      # ô đang hiển thị đến vị trí thứ idx
    "last_tick": 0,      # thời điểm cập nhật ô cuối
    "done_tick": 0,      # thời điểm animation hoàn thành
    "phase":     "scan", # "scan" → đang tô từng ô | "hold" → đã xong, đang giữ
    "next_move": None,   # vị trí tiếp theo sẽ áp dụng sau animation
    "is_pred":   True,   # True = đang visualize cho predator, False = prey
    "step_idx":  0,      # bước thứ mấy trong predator multi-step
    "predator_steps": 1, # tổng số bước predator trong lượt này
    "old_predator":   None,
    "cell_delay": VIS_CELL_DELAY,
    "hold_after": VIS_HOLD_AFTER,
    "path_display": VIS_PATH_DISPLAY,
}


# HANDLER
def handle_menu_click(pos):
    global state
    if btn_rect.collidepoint(pos):
        log("CLICK START -> CONFIG")
        state = STATE_CONFIG


def caught(predator, prey, catch_range=1):
    return abs(predator[0] - prey[0]) + abs(predator[1] - prey[1]) <= catch_range


def run_algo_and_start_vis(current_grid, agent_pos, opp_pos, algo_fn, is_pred,
                           extra_arg=None):
    """
    Chạy thuật toán, lấy kết quả + visited cells, bắt đầu phase animation.
    Trả về vị trí tiếp theo.
    """
    tracker.clear()
    try:
        if extra_arg is not None:
            next_pos = algo_fn(current_grid, agent_pos, opp_pos, extra_arg)
        else:
            next_pos = algo_fn(current_grid, agent_pos, opp_pos)
    except TypeError:
        next_pos = algo_fn(current_grid, agent_pos, opp_pos)

    all_v, all_p = tracker.get_all()

    # Giới hạn số ô hiển thị để không quá chậm trên bản đồ lớn
    grid_size  = len(current_grid)
    max_cells  = max(20, min(len(all_v), grid_size * grid_size // 4))
    cells_show = all_v[:max_cells]

    vis["active"]    = True
    vis["cells"]     = cells_show
    vis["path"]      = all_p
    vis["idx"]       = 0
    vis["last_tick"] = pygame.time.get_ticks()
    vis["done_tick"] = 0
    vis["phase"]     = "scan"
    vis["next_move"] = next_pos
    vis["is_pred"]   = is_pred

    # Bắt đầu hiển thị ô đầu tiên ngay lập tức
    tracker.set_display(cells_show[:1], [])
    _, _, score_map = tracker.get_display()
    if score_map:
        vis["cell_delay"] = VIS_CELL_DELAY_SLOW
        vis["hold_after"] = VIS_HOLD_AFTER_SLOW
        vis["path_display"] = VIS_PATH_DISPLAY_SLOW
    else:
        vis["cell_delay"] = VIS_CELL_DELAY
        vis["hold_after"] = VIS_HOLD_AFTER
        vis["path_display"] = VIS_PATH_DISPLAY
    return next_pos


# MAIN LOOP
running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_menu_click(event.pos)

        elif state == STATE_CONFIG:
            if event.type == pygame.KEYDOWN:
                handle_config_key(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = handle_config_click(event.pos, buttons, dropdowns, config)
                if result == "START":
                    log("START SIM")
                    state      = STATE_SIM
                    step_delay = 800

                    # RESET SIM
                    sim = {
                        "predator":          (0, 0),
                        "prey":              (4, 4),
                        "time":              0,
                        "running":           True,
                        "turn":              "predator",
                        "predator_last_dir": None,
                    }
                    grid = config["matrix"]
                    tracker.clear()
                    tracker.set_display([], [])
                    vis["active"] = False

                    # tạo vật cản động
                    if config.get("dynamic_obstacle"):
                        dyn_manager = DynamicObstacleManager(grid, seed=42, update_interval=3)
                        log("DYNAMIC OBSTACLE ENABLED (seed=42, interval=3)")
                    else:
                        dyn_manager = None

        elif state == STATE_SIM:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_btn.click(event.pos):
                    sim["running"] = not sim["running"]
                    log("PAUSE TOGGLE")
                    last_step = pygame.time.get_ticks()
                if end_btn.click(event.pos):
                    state = STATE_CONFIG
                    tracker.clear()
                    tracker.set_display([], [])
                    vis["active"] = False
                    log("END -> CONFIG")

    # ── UPDATE ──────────────────────────────────────────────────────────────
    if state == STATE_SIM and sim and sim["running"]:

        current_grid = dyn_manager.get_effective_grid() if dyn_manager else grid

        # ── Phase 1: Animation từng ô ──────────────────────────────────────
        if vis["active"]:
            if vis["phase"] == "scan":
                # Tô từng ô theo cell_delay (chậm hơn nếu có score hiển thị)
                if now - vis["last_tick"] >= vis["cell_delay"]:
                    vis["idx"]       += 1
                    vis["last_tick"]  = now

                    if vis["idx"] >= len(vis["cells"]):
                        # Scan xong → chuyển sang hold, giữ visited rồi mới hiển thị path
                        vis["phase"]     = "hold"
                        vis["done_tick"] = now
                        tracker.set_display(vis["cells"], [])
                    else:
                        # Hiện thêm 1 ô
                        tracker.set_display(vis["cells"][:vis["idx"]], [])

            elif vis["phase"] == "hold":
                # Đợi hold_after ms rồi hiển thị path
                if now - vis["done_tick"] >= vis["hold_after"]:
                    vis["phase"] = "path"
                    vis["done_tick"] = now
                    tracker.set_display(vis["cells"], vis["path"])

            elif vis["phase"] == "path":
                # Đợi path_display ms rồi áp dụng nước đi
                if now - vis["done_tick"] >= vis["path_display"]:
                    # --- Áp dụng nước đi ---
                    if vis["is_pred"]:
                        old_pred = sim["predator"]
                        sim["predator"] = vis["next_move"]
                        dr = sim["predator"][0] - old_pred[0]
                        dc = sim["predator"][1] - old_pred[1]
                        if (dr, dc) != (0, 0):
                            sim["predator_last_dir"] = (dr, dc)

                        if caught(sim["predator"], sim["prey"]):
                            sim["running"] = False
                            vis["active"]  = False
                            tracker.set_display([], [])
                        else:
                            # Kiểm tra còn bước nào không (multi-step predator)
                            vis["step_idx"] += 1
                            if vis["step_idx"] < vis["predator_steps"]:
                                # Chạy bước tiếp theo của predator
                                algo = selectAlgorithm(config["predator_algo"])
                                run_algo_and_start_vis(
                                    current_grid,
                                    sim["predator"],
                                    sim["prey"],
                                    algo,
                                    is_pred=True,
                                    extra_arg=sim["predator_last_dir"]
                                )
                            else:
                                # Hết bước predator → đến lượt prey
                                sim["turn"]   = "prey"
                                vis["active"] = False
                                tracker.set_display([], [])
                                last_step = now
                    else:
                        # Prey vừa animation xong
                        old_prey    = sim["prey"]
                        sim["prey"] = vis["next_move"]
                        if caught(sim["predator"], sim["prey"], catch_range=0):
                            sim["running"] = False
                        elif caught(sim["predator"], sim["prey"]):
                            sim["running"] = False
                        if sim["running"]:
                            sim["turn"] = "predator"
                        vis["active"] = False
                        tracker.set_display([], [])
                        sim["time"] += 1
                        last_step = now

        # ── Phase 2: Khởi động bước mới (sau step_delay) ─────────────────
        elif now - last_step > step_delay:
            # Cập nhật vật cản động
            if dyn_manager:
                dyn_manager.update(sim["time"], sim["predator"], sim["prey"])
            current_grid = dyn_manager.get_effective_grid() if dyn_manager else grid

            if sim["turn"] == "predator":
                predator_steps = config.get("predator_steps", 2)
                algo = selectAlgorithm(config["predator_algo"])
                vis["step_idx"]       = 0
                vis["predator_steps"] = predator_steps
                run_algo_and_start_vis(
                    current_grid,
                    sim["predator"],
                    sim["prey"],
                    algo,
                    is_pred=True,
                    extra_arg=sim["predator_last_dir"]
                )
            else:
                algo = selectAlgorithm(config["prey_algo"])
                run_algo_and_start_vis(
                    current_grid,
                    sim["prey"],
                    sim["predator"],
                    algo,
                    is_pred=False
                )

    # ── VẼ ──────────────────────────────────────────────────────────────────
    screen.fill((0, 0, 0))

    if state == STATE_MENU:
        btn_rect = draw_menu(screen, font, title_font, btn_rect)

    elif state == STATE_CONFIG:
        draw_config(screen, font, buttons, dropdowns, config)

    elif state == STATE_SIM and sim:
        current_grid = dyn_manager.get_effective_grid() if dyn_manager else grid
        draw_grid(screen, current_grid)
        draw_agents(screen, sim["predator"], sim["prey"], len(grid))
        draw_sim_ui(screen, font, sim)
        pause_btn.draw(screen, font)
        end_btn.draw(screen, font)

        if not sim["running"]:
            draw_game_over(screen, font, title_font)

    pygame.display.flip()

pygame.quit()