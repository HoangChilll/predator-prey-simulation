import pygame

# SCREEN

WIDTH = 800
HEIGHT = 600
GRID_AREA = int(WIDTH * 0.75)
FPS = 60



# CELL CALC 

def get_cell(size):
    return GRID_AREA // size


# VALID CHECK

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

def draw_agents(screen, prey, predator, size):
    cell = get_cell(size)
    # PREY (green)
    if valid(prey, size):
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (
                prey[1] * cell + cell // 2,
                prey[0] * cell + cell // 2
            ),
            cell // 3
        )

    # PREDATOR (red)
    if valid(predator, size):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (
                predator[1] * cell + cell // 2,
                predator[0] * cell + cell // 2
            ),
            cell // 3
        )