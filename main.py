import pygame
from ui.map import  draw_grid, draw_agents, font, title_font, btn_rect, buttons, dropdowns
from ui.stage1 import draw_menu
from ui.constants import WIDTH, HEIGHT,log
from ui.stage2 import get_config, draw_config, handle_config_click, selectMatrix
from ui.button import pause_btn, end_btn
from algorithm.selectalgorithm import selectAlgorithm
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

                    #  RESET SIM
                    sim = {
                        "grey": (8, 9),
                        "prey": (0, 0),
                        "time": 0,
                        "running": True,
                        "turn": "grey",
                        "grey_last_dir": None  # track last direction for momentum
                    }

                    grid = selectMatrix(config["grid"])
        elif state == STATE_SIM:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("CLICK AT:", event.pos) 
                if pause_btn.click(event.pos):
                  print("PAUSE CLICKED")
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

            if sim["turn"] == "grey":
                algo = selectAlgorithm(config["grey_algo"])
                old_grey = sim["grey"]
                # truyền last_dir nếu algo là grey_A* (nhận 4 tham số)
                try:
                    sim["grey"] = algo(grid, old_grey, sim["prey"], sim["grey_last_dir"])
                except TypeError:
                    sim["grey"] = algo(grid, old_grey, sim["prey"])
                # cập nhật last_dir
                dr = sim["grey"][0] - old_grey[0]
                dc = sim["grey"][1] - old_grey[1]
                sim["grey_last_dir"] = (dr, dc) if (dr, dc) != (0, 0) else sim["grey_last_dir"]
                print("GREY:", sim["grey"])
                if caught(sim["grey"], sim["prey"]):
                    sim["running"] = False
                    print("GAME OVER - Prey caught grey!")
                else:
                    sim["turn"] = "prey"

            else:
                for _ in range(2):
                    sim["prey"] = selectAlgorithm(config["prey_algo"])(grid, sim["prey"], sim["grey"])
                    print("PREY:", sim["prey"])
                    # Chỉ break giữa chừng khi đứng TRÙNG ô (range=0)
                    # tránh break sớm khi chỉ liền kề grey sau bước 1
                    if caught(sim["grey"], sim["prey"], catch_range=0):
                        sim["running"] = False
                        print("GAME OVER - Prey caught grey!")
                        break
                # Sau khi đi đủ 2 bước, mới check liền kề (range=1)
                if sim["running"] and caught(sim["grey"], sim["prey"]):
                    sim["running"] = False
                    print("GAME OVER - Prey caught grey!")
                if sim["running"]:
                    sim["turn"] = "grey"
            sim["time"] += 1
            last_step = now

    # vẽ
    screen.fill((0, 0, 0))

    if state == STATE_MENU:
        btn_rect = draw_menu(screen, font, title_font, btn_rect)

    elif state == STATE_CONFIG:
        draw_config(screen, font, buttons, dropdowns)

    elif state == STATE_SIM and sim:
        draw_grid(screen, grid)
        draw_agents(screen, sim["grey"], sim["prey"], len(grid))

        # TIME
        txt = font.render(f"Time: {sim['time']}", True, (255,255,255))
        screen.blit(txt, (WIDTH - 200, 50))

        # TURN
        txt2 = font.render(f"Turn: {sim['turn']}", True, (255,255,255))
        screen.blit(txt2, (WIDTH - 200, 100))

        pause_btn.draw(screen, font)
        end_btn.draw(screen, font)

        if not sim["running"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            go_text = title_font.render("GAME OVER", True, (255, 80, 80))
            screen.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            sub_text = font.render("Predator caught prey!", True, (255, 255, 255))
            screen.blit(sub_text, sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

    pygame.display.flip()

pygame.quit()