import math
import pygame
from config import ColorConfig
from ui.effects import EffectsState

class Renderer:
    def __init__(self, grid, simulator, cell_size):
        self.grid = grid
        self.simulator = simulator
        self.cell_size = cell_size

    def draw(self, screen, offset_x=0, offset_y=0):
        # Draw grid
        for i in range(len(self.grid.cells)):
            for j in range(len(self.grid.cells[0])):
                cell = self.grid.cells[i][j]

                offset = math.sin(EffectsState.animation_time * 0.01 + (i + j) * 0.1) * 0.5
                
                rect = pygame.Rect(
                    offset_x + j * self.cell_size,
                    offset_y + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Draw empty cells / walls
                if cell == self.grid.WALL:
                    color = ColorConfig.WALL
                    pygame.draw.rect(screen, color, rect)
                else:
                    grid_color = (200 + int(offset * 10), 200 + int(offset * 10), 200 + int(offset * 10))
                    pygame.draw.rect(screen, grid_color, rect, 1)

        # Draw Predator
        if self.simulator.predators:
            for pred in self.simulator.predators:
                predator_bob = math.sin(EffectsState.animation_time * 0.05) * 3
                predator_rect = pygame.Rect(
                    offset_x + pred[1] * self.cell_size,
                    offset_y + pred[0] * self.cell_size + predator_bob,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 0, 0), predator_rect)
                pygame.draw.rect(screen, (255, 100, 100), predator_rect, 3)

        # Draw Prey
        if self.simulator.preys:
            for prey in self.simulator.preys:
                grey_bob = math.sin(EffectsState.animation_time * 0.04 + 1) * 3
                grey_rect = pygame.Rect(
                    offset_x + prey[1] * self.cell_size,
                    offset_y + prey[0] * self.cell_size + grey_bob,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (130, 130, 130), grey_rect)
                pygame.draw.rect(screen, (180, 180, 180), grey_rect, 3)