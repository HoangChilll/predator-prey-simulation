 # vẽ grid bằng pygame
import pygame
from config import ColorConfig

class Renderer:
    def __init__(self, grid, simulator, cell_size):
        self.grid = grid
        self.simulator = simulator
        self.cell_size = cell_size

    # =========================
    # DRAW ALL
    # =========================
    def draw(self, screen):
        for i in range(len(self.grid.cells)):
            for j in range(len(self.grid.cells[0])):
                cell = self.grid.cells[i][j]

                rect = (
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                if cell == self.grid.EMPTY:
                    color = ColorConfig.EMPTY_CELL
                elif cell == self.grid.WALL:
                    color = ColorConfig.WALL
                elif cell == self.grid.PREDATOR:
                    color = ColorConfig.PREDATOR
                elif cell == self.grid.PREY:
                    color = ColorConfig.PREY

                pygame.draw.rect(screen, color, rect)

                # 🔥 vẽ viền cho dễ nhìn
                pygame.draw.rect(screen, ColorConfig.GRID_BORDER, rect, 1)