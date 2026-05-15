import pygame

from ui.stage2 import create_ui
from ui.constants import WIDTH, HEIGHT, GRID_AREA
# SCREEN
pygame.init()
font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 40)
btn_rect = pygame.Rect(220, 200, 160, 60)
buttons, dropdowns = create_ui()


# CELL CALC 

def get_cell(size):
    return GRID_AREA // size

def valid(pos, size):
    return True
# DRAW GRID

def draw_grid(screen, grid):
    size = len(grid)
    cell = get_cell(size)

    for row in range(size):
        for col in range(size):
            rect = pygame.Rect(
                col * cell,
                row * cell,
                cell,
                cell
            )

            if grid[row][col] == 1:
                color = (80, 80, 80)   # path
            else:
                color = (30, 30, 30)   # wall

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)


# DRAW AGENTS (FIXED)

def draw_agents(screen, grey, prey, size):
    cell = get_cell(size)
    # GREY (green)
    if valid(grey, size):
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (
                grey[1] * cell + cell // 2,
                grey[0] * cell + cell // 2
            ),
            cell // 3
        )

    # PREY (red)
    if valid(prey, size):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (
                prey[1] * cell + cell // 2,
                prey[0] * cell + cell // 2
            ),
            cell // 3
        )