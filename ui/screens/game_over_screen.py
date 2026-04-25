import math
import pygame
from ui.effects import EffectsState, draw_animated_background, draw_particles, create_particle
from ui.components import title_font, button_font, small_font, draw_button, get_button_scale, draw_exit_button
from config import ScreenConfig
from core.grid import Grid


class GameOverScreen:
    def __init__(self, result):
        """
        result = {
            "grid_size": int,
            "grid_cells": 2D list (snapshot of the map),
            "predator_strategy": str,
            "prey_strategy": str,
            "predator_steps": int,
            "predator_pos": (x, y),
            "prey_pos": (x, y) or None,
        }
        """
        self.result = result

        # Buttons
        self.menu_button = pygame.Rect(400, 640, 200, 60)
        self.exit_button = pygame.Rect(920, 20, 50, 50)

        # Precompute mini-map dimensions
        self.grid_size = result["grid_size"]
        self.grid_cells = result["grid_cells"]

        # Fit the mini-map into a fixed area
        self.map_area_size = 300
        self.cell_size = self.map_area_size // self.grid_size

        # Center the mini-map
        self.map_x = (ScreenConfig.WIDTH - self.cell_size * self.grid_size) // 2
        self.map_y = 265

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.collidepoint(event.pos):
                    return "QUIT"
                if self.menu_button.collidepoint(event.pos):
                    EffectsState.particles.clear()
                    return "MENU"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    EffectsState.particles.clear()
                    return "MENU"
        return None

    def update(self):
        pass

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # === Animated background ===
        draw_animated_background(
            screen,
            ScreenConfig.WIDTH,
            ScreenConfig.HEIGHT,
            EffectsState.animation_time * 2,
            EffectsState.animation_time,
        )
        draw_particles(screen)

        if EffectsState.animation_time % 5 == 0:
            create_particle(mouse_pos[0], mouse_pos[1])

        # === Dark overlay ===
        overlay = pygame.Surface((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((10, 10, 30))
        screen.blit(overlay, (0, 0))

        # === Title with bounce ===
        title_y = 45 + math.sin(EffectsState.animation_time * 0.025) * 4
        title_text = title_font.render("PREY CAUGHT!", True, (255, 80, 80))
        title_rect = title_text.get_rect(center=(ScreenConfig.WIDTH // 2, title_y))
        screen.blit(title_text, title_rect)

        # === Subtitle ===
        subtitle_text = small_font.render(
            "The predator successfully captured the prey", True, (220, 220, 220)
        )
        subtitle_rect = subtitle_text.get_rect(center=(ScreenConfig.WIDTH // 2, 90))
        screen.blit(subtitle_text, subtitle_rect)

        # === Info panel ===
        info_y = 120
        line_height = 32

        # Grid size
        size_label = button_font.render(
            f"Map Size:  {self.grid_size} x {self.grid_size}", True, (255, 255, 255)
        )
        size_rect = size_label.get_rect(center=(ScreenConfig.WIDTH // 2, info_y))
        screen.blit(size_label, size_rect)
        info_y += line_height

        # Predator strategy
        pred_strat = self.result["predator_strategy"].upper()
        pred_label = button_font.render(
            f"Predator Strategy:  {pred_strat}", True, (255, 150, 150)
        )
        pred_rect = pred_label.get_rect(center=(ScreenConfig.WIDTH // 2, info_y))
        screen.blit(pred_label, pred_rect)
        info_y += line_height

        # Prey strategy
        prey_strat = self.result["prey_strategy"].upper()
        prey_label = button_font.render(
            f"Prey Strategy:  {prey_strat}", True, (150, 255, 150)
        )
        prey_rect = prey_label.get_rect(center=(ScreenConfig.WIDTH // 2, info_y))
        screen.blit(prey_label, prey_rect)
        info_y += line_height

        # Steps
        steps = self.result["predator_steps"]
        steps_label = button_font.render(
            f"Steps to Capture:  {steps}", True, (255, 220, 100)
        )
        steps_rect = steps_label.get_rect(center=(ScreenConfig.WIDTH // 2, info_y))
        screen.blit(steps_label, steps_rect)

        # === Mini-map ===
        map_label = small_font.render("Final Map State", True, (200, 200, 200))
        map_label_rect = map_label.get_rect(
            center=(ScreenConfig.WIDTH // 2, self.map_y - 20)
        )
        screen.blit(map_label, map_label_rect)

        predator_pos = self.result.get("predator_pos")
        prey_pos = self.result.get("prey_pos")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_val = self.grid_cells[i][j]
                rect = pygame.Rect(
                    self.map_x + j * self.cell_size,
                    self.map_y + i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                # Background color per cell type
                if cell_val == Grid.WALL:
                    color = (50, 50, 50)
                    pygame.draw.rect(screen, color, rect)
                else:
                    # Subtle wave for empty cells
                    wave = (
                        math.sin(
                            EffectsState.animation_time * 0.01 + (i + j) * 0.15
                        )
                        * 8
                    )
                    base = int(200 + wave)
                    base = max(180, min(220, base))
                    color = (base, base, base)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (160, 160, 160), rect, 1)

        # Draw predator marker
        if predator_pos:
            px, py = predator_pos
            pred_rect = pygame.Rect(
                self.map_x + py * self.cell_size,
                self.map_y + px * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            # Pulsing glow
            pulse = abs(math.sin(EffectsState.animation_time * 0.05)) * 55
            glow_color = (255, int(50 + pulse), int(50 + pulse))
            pygame.draw.rect(screen, glow_color, pred_rect)
            pygame.draw.rect(screen, (255, 200, 200), pred_rect, 2)

            # Label
            if self.cell_size >= 16:
                p_label = small_font.render("P", True, (255, 255, 255))
                p_rect = p_label.get_rect(center=pred_rect.center)
                screen.blit(p_label, p_rect)

        # Draw prey marker (last known position, even if caught)
        if prey_pos:
            gx, gy = prey_pos
            grey_rect = pygame.Rect(
                self.map_x + gy * self.cell_size,
                self.map_y + gx * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(screen, (130, 130, 130), grey_rect)
            pygame.draw.rect(screen, (180, 180, 180), grey_rect, 2)

            if self.cell_size >= 16:
                g_label = small_font.render("G", True, (255, 255, 255))
                g_rect = g_label.get_rect(center=grey_rect.center)
                screen.blit(g_label, g_rect)

        # Map border
        border_rect = pygame.Rect(
            self.map_x - 2,
            self.map_y - 2,
            self.cell_size * self.grid_size + 4,
            self.cell_size * self.grid_size + 4,
        )
        pygame.draw.rect(screen, (100, 100, 140), border_rect, 2, border_radius=3)

        # === Legend ===
        legend_y = self.map_y + self.cell_size * self.grid_size + 15

        # Predator legend
        pred_legend_rect = pygame.Rect(ScreenConfig.WIDTH // 2 - 160, legend_y, 18, 18)
        pygame.draw.rect(screen, (255, 80, 80), pred_legend_rect)
        pred_legend_text = small_font.render("Predator", True, (255, 150, 150))
        screen.blit(pred_legend_text, (pred_legend_rect.right + 6, legend_y - 1))

        # Prey legend
        prey_legend_rect = pygame.Rect(ScreenConfig.WIDTH // 2 + 40, legend_y, 18, 18)
        pygame.draw.rect(screen, (130, 130, 130), prey_legend_rect)
        prey_legend_text = small_font.render("Prey", True, (150, 255, 150))
        screen.blit(prey_legend_text, (prey_legend_rect.right + 6, legend_y - 1))

        # Wall legend
        wall_legend_rect = pygame.Rect(ScreenConfig.WIDTH // 2 + 170, legend_y, 18, 18)
        pygame.draw.rect(screen, (50, 50, 50), wall_legend_rect)
        wall_legend_text = small_font.render("Wall", True, (180, 180, 180))
        screen.blit(wall_legend_text, (wall_legend_rect.right + 6, legend_y - 1))

        # === Back to Menu button ===
        hover = self.menu_button.collidepoint(mouse_pos)
        btn_color = (255, 140, 0) if hover else (220, 120, 0)
        scale = get_button_scale(hover)
        draw_button(
            screen, self.menu_button, "Back to Menu", btn_color, radius=12, scale=scale
        )

        # === Exit button ===
        draw_exit_button(screen, self.exit_button, mouse_pos)
