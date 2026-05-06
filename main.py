import pygame
from ui.map import WIDTH, HEIGHT, draw_grid, draw_agents
from ui.stage1 import draw_menu
from ui.stage2 import get_config, create_ui, draw_config, handle_config_click
from log import log
from algorithm.random import random_move  
from ui.grid import grid10x10,grid50x50,grid40,grid20x20_2
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


# UI
font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 40)
btn_rect = pygame.Rect(220, 200, 160, 60)
buttons, dropdowns = create_ui()

# SIM INIT (placeholder)
sim = None  #trạng thái
grid = grid20x20_2#ma trận môi trường

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

    # ===== EVENTS =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===== MENU =====
        if state == STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_menu_click(event.pos)

        # ===== CONFIG =====
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
                        "prey": (8, 9),
                        "predator": (0, 0),
                        "time": 0,
                        "running": True,
                        "turn": "prey"  
                    }

                    #grid = [[1] * config["size"] for _ in range(config["size"])]
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
    # ===== UPDATE (KHÔNG ĐỂ TRONG EVENT) =====
    if state == STATE_SIM and sim:
        if sim["running"] and now - last_step > step_delay:

            if sim["turn"] == "prey":
                sim["prey"] = selectAlgorithm(config["prey_algo"])(grid, sim["prey"], sim["predator"])
                print("PREY:", sim["prey"])  # in tọa độ prey
                sim["turn"] = "predator"
                

            else:
                sim["predator"] = selectAlgorithm(config["grey_algo"])(grid, sim["predator"], sim["prey"])
                print("PREDATOR:", sim["predator"])  # in tọa độ predator
                sim["turn"] = "prey"
            # 2 agents gặp nhau
            if sim["prey"] == sim["predator"]:
               sim["running"] = False
               print("GAME OVER")
            sim["time"] += 1
            last_step = now

    # ===== DRAW =====
    screen.fill((0, 0, 0))

    if state == STATE_MENU:
        btn_rect = draw_menu(screen, font, title_font, btn_rect)

    elif state == STATE_CONFIG:
        draw_config(screen, font, buttons, dropdowns)

    elif state == STATE_SIM and sim:
        draw_grid(screen, grid)
        draw_agents(screen, sim["prey"], sim["predator"], config["size"])

        # TIME
        txt = font.render(f"Time: {sim['time']}", True, (255,255,255))
        screen.blit(txt, (WIDTH - 200, 50))

        # TURN
        txt2 = font.render(f"Turn: {sim['turn']}", True, (255,255,255))
        screen.blit(txt2, (WIDTH - 200, 100))

        pause_btn.draw(screen, font)
        end_btn.draw(screen, font)

    pygame.display.flip()

pygame.quit()