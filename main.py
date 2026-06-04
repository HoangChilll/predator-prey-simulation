import pygame
from ui.map import  draw_grid, draw_agents, draw_sim_ui, draw_game_over, font, title_font, btn_rect, buttons, dropdowns
from ui.stage1 import draw_menu
from ui.constants import WIDTH, HEIGHT,log
from ui.stage2 import get_config, draw_config, handle_config_click, handle_config_key, selectMatrix
from ui.button import pause_btn, end_btn
from algorithm.selectalgorithm import selectAlgorithm
from algorithm.dynamic_obstacles import DynamicObstacleManager
# STAGE


STATE_MENU = 1
STATE_CONFIG = 2
STATE_SIM = 3

config = get_config()
state = STATE_MENU

# INIT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()





# Các tham số ban đầu
sim = None  #trạng thái
grid = None
dyn_manager = None  # DynamicObstacleManager, None khi tắt chế độ dynamic

step_delay = 1000
last_step = pygame.time.get_ticks()

# HANDLER
def handle_menu_click(pos):
    global state
    if btn_rect.collidepoint(pos):
        log("CLICK START -> CONFIG")
        state = STATE_CONFIG

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
                result = handle_config_click(
                    event.pos,
                    buttons,
                    dropdowns,
                    config
                )

                if result == "START":
                    log("START SIM")

                    state = STATE_SIM
                    step_delay = 1000 + (config.get("prey_steps", 2) - 1) * 300

                    #  RESET SIM
                    sim = {
                        "grey": (8, 9),
                        "prey": (0, 0),
                        "time": 0,
                        "running": True,
                        "turn": "grey",
                        "grey_last_dir": None
                    }

                    grid = config["matrix"]

                    # Khởi tạo dynamic obstacle layer (seed=42 đảm bảo reproducible)
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
                  log("END -> CONFIG")
    #  UPDATE
    if state == STATE_SIM and sim:
        if sim["running"] and now - last_step > step_delay:

            def caught(grey, prey, catch_range=1):
                return abs(grey[0] - prey[0]) + abs(grey[1] - prey[1]) <= catch_range

            # Cập nhật vật cản động (chỉ khi đến interval, sau bước 0)
            if dyn_manager:
                dyn_manager.update(sim["time"], sim["grey"], sim["prey"])

            # Grid hiệu dụng: chứa cả vật cản động (value=2) nếu bật
            current_grid = dyn_manager.get_effective_grid() if dyn_manager else grid

            if sim["turn"] == "grey":
                algo = selectAlgorithm(config["grey_algo"])
                old_grey = sim["grey"]
                # truyền last_dir nếu algo là grey_A* (nhận 4 tham số)
                try:
                    sim["grey"] = algo(current_grid, old_grey, sim["prey"], sim["grey_last_dir"])
                except TypeError:
                    sim["grey"] = algo(current_grid, old_grey, sim["prey"])
                # cập nhật last_dir
                dr = sim["grey"][0] - old_grey[0]
                dc = sim["grey"][1] - old_grey[1]
                sim["grey_last_dir"] = (dr, dc) if (dr, dc) != (0, 0) else sim["grey_last_dir"]
                if caught(sim["grey"], sim["prey"]):
                    sim["running"] = False
                else:
                    sim["turn"] = "prey"

            else:
                for _ in range(config.get("prey_steps", 2)):
                    sim["prey"] = selectAlgorithm(config["prey_algo"])(current_grid, sim["prey"], sim["grey"])
                    # Chỉ break giữa chừng khi đứng TRÙNG ô (range=0)
                    if caught(sim["grey"], sim["prey"], catch_range=0):
                        sim["running"] = False
                        break
                # Sau khi đi đủ tất cả bước, mới check liền kề (range=1)
                if sim["running"] and caught(sim["grey"], sim["prey"]):
                    sim["running"] = False
                if sim["running"]:
                    sim["turn"] = "grey"
            sim["time"] += 1
            last_step = now

    # vẽ
    screen.fill((0, 0, 0))

    if state == STATE_MENU:
        btn_rect = draw_menu(screen, font, title_font, btn_rect)

    elif state == STATE_CONFIG:
        draw_config(screen, font, buttons, dropdowns, config)

    elif state == STATE_SIM and sim:
        current_grid = dyn_manager.get_effective_grid() if dyn_manager else grid
        draw_grid(screen, current_grid)
        draw_agents(screen, sim["grey"], sim["prey"], len(grid))
        draw_sim_ui(screen, font, sim)
        pause_btn.draw(screen, font)
        end_btn.draw(screen, font)

        if not sim["running"]:
            draw_game_over(screen, font, title_font)

    pygame.display.flip()

pygame.quit()