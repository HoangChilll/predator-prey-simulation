import pygame
from ui.button import Button

from ui.constants import WIDTH, HEIGHT, log

_FONTS = {}
def _f(size):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("Arial", size)
    return _FONTS[size]
from ui.grid import grid5x5,grid10x10,grid20x20_2 ,MAZE_20,grid20x20, grid40x40,grid40x40_2
from ui.dropdown import Dropdown, toggle_dropdown, update_dropdown
from algorithm.random_maze import generate_random_maze

# Trạng thái kích thước mê cung ngẫu nhiên (điều chỉnh qua nút +/-)
_rand_size = {"value": 20}
_BTN_SZ = 36
_RAND_CTR_Y = int(HEIGHT * 0.50)
_RAND_MINUS_RECT = pygame.Rect(WIDTH // 2 - 80, _RAND_CTR_Y, _BTN_SZ, _BTN_SZ)
_RAND_VAL_RECT   = pygame.Rect(WIDTH // 2 - 30, _RAND_CTR_Y, 60, _BTN_SZ)
_RAND_PLUS_RECT  = pygame.Rect(WIDTH // 2 + 34, _RAND_CTR_Y, _BTN_SZ, _BTN_SZ)


MATRICES = {
    "5": grid5x5,
    "10_1": grid10x10,
    "20_2": grid20x20_2,
    "20": MAZE_20,
    "20_1": grid20x20,
    "40": grid40x40,
    "40_2": grid40x40_2

    
 
}

def selectMatrix(name):
    if name not in MATRICES:
        raise ValueError(f"Matrix '{name}' không tồn tại")
    
    return MATRICES[name]



def get_config():
    cfg = {
        "grid": "10_1",
        "predator_algo": "pred_greedy",
        "prey_algo": "random",
        "predator_steps": 2,
        "dynamic_obstacle": False
    }
    log(f"INIT CONFIG: {cfg}")
    return cfg



# UI RENDER

def _draw_rand_controls(screen, font):
    lbl = _f(18).render("Kích thước mê cung  (11 – 40)", True, (145, 175, 225))
    screen.blit(lbl, lbl.get_rect(center=(WIDTH // 2, _RAND_CTR_Y - 24)))

    mouse_pos = pygame.mouse.get_pos()
    for rect, sym in [(_RAND_MINUS_RECT, "-"), (_RAND_PLUS_RECT, "+")]:
        hover = rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (0, 0, 0), rect.move(3, 3), border_radius=9)
        pygame.draw.rect(screen, (55, 88, 195) if hover else (35, 62, 165), rect, border_radius=9)
        sheen = pygame.Surface((rect.width - 6, rect.height // 2 - 2), pygame.SRCALPHA)
        sheen.fill((255, 255, 255, 18))
        screen.blit(sheen, (rect.x + 3, rect.y + 3))
        pygame.draw.rect(screen, (120, 160, 255) if hover else (75, 110, 220),
                         rect, width=2, border_radius=9)
        t = font.render(sym, True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=rect.center))

    # Value display
    pygame.draw.rect(screen, (0, 0, 0), _RAND_VAL_RECT.move(3, 3), border_radius=7)
    pygame.draw.rect(screen, (28, 32, 58), _RAND_VAL_RECT, border_radius=7)
    pygame.draw.rect(screen, (100, 130, 210), _RAND_VAL_RECT, width=2, border_radius=7)
    vs = font.render(str(_rand_size["value"]), True, (220, 225, 255))
    screen.blit(vs, vs.get_rect(center=_RAND_VAL_RECT.center))


def draw_config(screen, font, buttons, dropdowns, config=None):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(10 + ratio * 8)
        g = int(10 + ratio * 6)
        b = int(32 + ratio * 22)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    gs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH + 1, 55):
        pygame.draw.line(gs, (65, 88, 155, 13), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT + 1, 55):
        pygame.draw.line(gs, (65, 88, 155, 13), (0, y), (WIDTH, y))
    screen.blit(gs, (0, 0))

    # vẽ panel
    pm = 38
    pr = pygame.Rect(pm, pm, WIDTH - 2*pm, HEIGHT - 2*pm)
    ps = pygame.Surface((pr.width, pr.height), pygame.SRCALPHA)
    pygame.draw.rect(ps, (16, 20, 40, 210), ps.get_rect(), border_radius=18)
    pygame.draw.rect(ps, (75, 108, 200, 240), ps.get_rect(), width=2, border_radius=18)
    screen.blit(ps, (pm, pm))

    # vẽ tiêu đề
    title_cy = int(HEIGHT * 0.10)
    sh = font.render("CONFIGURATION", True, (0, 0, 0))
    screen.blit(sh, sh.get_rect(center=(WIDTH // 2 + 3, title_cy + 3)))
    title_s = font.render("CONFIGURATION", True, (255, 210, 55))
    screen.blit(title_s, title_s.get_rect(center=(WIDTH // 2, title_cy)))

    # vẽ đường kẻ dưới tiêu đề
    lw, ly, mx = 180, title_cy + title_s.get_height() // 2 + 14, WIDTH // 2
    pygame.draw.line(screen, (70, 108, 198), (mx - lw//2, ly), (mx - 10, ly - 7), 2)
    pygame.draw.line(screen, (255, 210, 55), (mx - 10, ly - 7), (mx + 10, ly - 7), 2)
    pygame.draw.line(screen, (70, 108, 198), (mx + 10, ly - 7), (mx + lw//2, ly), 2)

    # vẽ nút
    row1_meta = [
        ("PREDATOR ALGORITHM",  "pred"),
        ("PREY ALGORITHM",      "prey"),
        ("MAP LAYOUT",          "grid"),
        ("PREDATOR STEPS",      None),
    ]
    for i, (lbl_text, dd_key) in enumerate(row1_meta):
        if i >= len(buttons):
            break
        btn = buttons[i]
        lbl_s = _f(16).render(lbl_text, True, (115, 148, 212))
        screen.blit(lbl_s, lbl_s.get_rect(center=(btn.rect.centerx, btn.rect.y - 14)))
        if dd_key and dd_key in dropdowns:
            sel_text = dropdowns[dd_key].selected
            sel_s = _f(15).render(sel_text, True, (170, 195, 245))
            screen.blit(sel_s, sel_s.get_rect(center=(btn.rect.centerx, btn.rect.bottom + 13)))
    if len(buttons) > 4:
        lbl_s = _f(16).render("OBSTACLES", True, (115, 148, 212))
        screen.blit(lbl_s, lbl_s.get_rect(center=(buttons[4].rect.centerx, buttons[4].rect.y - 14)))

    # vẽ bút
    for btn in buttons:
        btn.draw(screen, font)
    for dd in dropdowns.values():
        dd.draw(screen, font)

    # vẽ +- size
    if config and config.get("grid") == "random":
        _draw_rand_controls(screen, font)

    pygame.display.flip()



#hàm xử lý input
def handle_config_click(pos, buttons, dropdowns, config):
    # Xử lý nút +/- kích thước random
    if config.get("grid") == "random":
        if _RAND_MINUS_RECT.collidepoint(pos):
            _rand_size["value"] = max(11, _rand_size["value"] - 1)
            return None
        if _RAND_PLUS_RECT.collidepoint(pos):
            _rand_size["value"] = min(40, _rand_size["value"] + 1)
            return None

    for btn in buttons:

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        btn.update(mouse_pos, mouse_down)

        if btn.click(pos):

            log(f"CLICK BUTTON: {btn.text}")

            
            if btn.text == "PREY":
                toggle_dropdown(dropdowns, "prey")


            elif btn.text.lower() == "pred":
                toggle_dropdown(dropdowns, "pred")


            elif btn.text == "GRID":
                toggle_dropdown(dropdowns, "grid")

            elif btn.text.startswith("Steps:"):
                config["predator_steps"] = (config["predator_steps"] % 3) + 1
                btn.text = f"Steps:{config['predator_steps']}"
                log(f"PREDATOR STEPS SET TO: {config['predator_steps']}")

            elif "Dynamic" in btn.text:
                config["dynamic_obstacle"] = not config.get("dynamic_obstacle", False)
                btn.text = "[X] Dynamic" if config["dynamic_obstacle"] else "[ ] Dynamic"
                log(f"DYNAMIC OBSTACLE: {config['dynamic_obstacle']}")


            elif btn.text == "START":
                if config["grid"] == "random":
                    config["matrix"] = generate_random_maze(_rand_size["value"])
                else:
                    config["matrix"] = selectMatrix(config["grid"])

                log(f"START GAME WITH CONFIG: {config}")

                return "START"

    

    update_dropdown(config, dropdowns, "prey", "prey_algo")

    update_dropdown(config, dropdowns, "pred", "predator_algo")

    update_dropdown(config, dropdowns, "grid", "grid")

    return None





def create_ui():
    btn_width = 120
    btn_height = 40
    btn_spacing = 50

    # Hàng 1: 4 nút tùy chọn (PRED, PREY, GRID, Steps)
    n_row1 = 4
    total_row1_w = n_row1 * btn_width + (n_row1 - 1) * btn_spacing
    row1_x = (WIDTH - total_row1_w) // 2
    row1_y = int(HEIGHT * 0.23)

    buttons = []
    for i, text in enumerate(["PRED", "PREY", "GRID", "Steps:2"]):
        x = row1_x + i * (btn_width + btn_spacing)
        buttons.append(Button(x, row1_y, btn_width, btn_height, text))

    # Hàng 2: nút Dynamic (index 4) và START (index 5) đặt cạnh nhau, căn giữa
    row2_y = int(HEIGHT * 0.72)
    dyn_w = 160
    gap = 20
    row2_total = dyn_w + gap + btn_width
    row2_x = (WIDTH - row2_total) // 2

    buttons.append(Button(row2_x, row2_y, dyn_w, btn_height, "[ ] Dynamic"))          # index 4
    buttons.append(Button(row2_x + dyn_w + gap, row2_y, btn_width, btn_height, "START"))  # index 5

    dropdowns = {
        "prey": Dropdown(
            ["random", "prey_greedy", "prey_space_ap", "prey_weighted_evade", "prey_adaptive", "prey_minimax_shortest", "prey_minimax_euclid"],
            buttons[0].rect.x, buttons[0].rect.y + btn_height + 5
        ),
        "pred": Dropdown(
            ["random", "pred_greedy", "pred_dfs", "pred_control", "pred_a_star", "pred_bfs", "pred_minimax_shortest", "pred_minimax_euclid"],
            buttons[1].rect.x, buttons[1].rect.y + btn_height + 5
        ),
        "grid": Dropdown(
            ["5", "10_1", "20_2", "20_1", "20", "40", "40_2", "random"],
            buttons[2].rect.x, buttons[2].rect.y + btn_height + 5
        ),
    }
    log("UI CREATED (buttons + dropdowns)")
    return buttons, dropdowns


def handle_config_key(event):
    pass