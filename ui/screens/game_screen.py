import math
import pygame
from ui.controls import GameControls
from core.maps import get_random_map
from simulation.simulator import Simulator
from core.grid import Grid
from ui.render import Renderer
from agents.strategies.strategie_factory import get_predator_strategy, get_prey_strategy
from config import ScreenConfig
from ui.effects import EffectsState, draw_animated_background, draw_particles
from ui.components import title_font, button_font, small_font, draw_button, get_button_scale, draw_exit_button

class GameScreen:
    def __init__(self, config):
        # ===== CONFIG =====
        self.grid_size = config["grid_size"]
        self.predator_strategy_name = config["predator_strategy"]
        self.prey_strategy_name = config["prey_strategy"]
        self.predator_strategy = get_predator_strategy(self.predator_strategy_name)
        self.prey_strategy = get_prey_strategy(self.prey_strategy_name)

        # ===== TẠO GRID =====
        self.grid = Grid(self.grid_size, self.grid_size)

        # 🔥 LOAD MAP RANDOM
        map_data = get_random_map(self.grid_size)
        self.grid.load_map(map_data)

        # ===== SIMULATOR =====
        self.simulator = Simulator(
            self.grid,
            self.predator_strategy,
            self.prey_strategy
        )

        # ===== SPAWN AGENTS =====
        self.simulator.add_predator(0, 0)
        self.simulator.add_prey(self.grid_size - 1, self.grid_size - 1)

        # ===== RENDER =====
        self.grid_x = 80
        self.grid_y = 90
        self.grid_width = 550
        self.grid_height = 550
        self.cell_size = min(self.grid_width // self.grid_size, self.grid_height // self.grid_size)

        self.renderer = Renderer(
            self.grid,
            self.simulator,
            self.cell_size
        )

        # ===== STATE =====
        self.controls = GameControls(config)
        self.game_over = False
        self.game_over_timer = 0
        self.game_over_result = None

        self.pause_button = pygame.Rect(700, 400, 120, 55)
        self.stop_button = pygame.Rect(700, 480, 120, 55)
        self.back_button = pygame.Rect(40, 20, 140, 50)
        self.exit_button = pygame.Rect(920, 20, 50, 50)

    # =========================
    # EVENT
    # =========================
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.collidepoint(event.pos):
                    return "QUIT"
                
                if self.back_button.collidepoint(event.pos):
                    EffectsState.particles.clear()
                    return "MENU"

                if self.pause_button.collidepoint(event.pos):
                    self.controls.paused = not self.controls.paused

                if self.stop_button.collidepoint(event.pos):
                    EffectsState.particles.clear()
                    return "MENU"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.controls.paused = not self.controls.paused

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"

        # Tự động chuyển trang sau khi bắt được
        if self.game_over:
            self.game_over_timer += 1
            if self.game_over_timer > 120:  # 2 giây ở 60 FPS
                EffectsState.particles.clear()
                return ("GAME_OVER", self.game_over_result)
        else:
            control_result = self.controls.handle_events(events)
            if control_result:
                return control_result

        return None

    # =========================
    # UPDATE
    # =========================
    def update(self):
        if not self.game_over:
            result = self.controls.update(self.simulator)
            if not self.simulator.preys or (isinstance(result, tuple) and result[0] == "GAME_OVER"):
                self.game_over = True
                # Build result snapshot for game over screen
                import copy
                self.game_over_result = {
                    "grid_size": self.grid_size,
                    "grid_cells": copy.deepcopy(self.grid.cells),
                    "predator_strategy": self.predator_strategy_name,
                    "prey_strategy": self.prey_strategy_name,
                    "predator_steps": self.simulator.predator_steps,
                    "predator_pos": self.simulator.predators[0] if self.simulator.predators else None,
                    "prey_pos": self.simulator.preys[0] if self.simulator.preys else (
                        self.simulator.predators[0] if self.simulator.predators else None
                    ),
                }
            return result
        return None

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Animated background & Particles
        draw_animated_background(screen, ScreenConfig.WIDTH, ScreenConfig.HEIGHT, EffectsState.animation_time * 2, EffectsState.animation_time)
        draw_particles(screen)

        # Overlay
        overlay = pygame.Surface((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
        overlay.set_alpha(80)
        overlay.fill((30, 30, 30))
        screen.blit(overlay, (0, 0))

        panel_x = self.grid_x + self.grid_width + 40

        # Draw real grid and simulation
        self.renderer.draw(screen, offset_x=self.grid_x, offset_y=self.grid_y)

        # Title/info
        sim_title = title_font.render("Simulation", True, (255, 255, 255))
        screen.blit(sim_title, (panel_x, 120))

        info1 = button_font.render(f"Size: {self.grid_size}x{self.grid_size}", True, (255, 255, 255))
        info2 = button_font.render(f"Predator: {self.predator_strategy_name.upper()}", True, (255, 150, 150))
        info3 = button_font.render(f"Prey: {self.prey_strategy_name.upper()}", True, (150, 255, 150))
        info4 = small_font.render(f"Steps: {self.simulator.predator_steps}", True, (200, 200, 200))
        screen.blit(info1, (panel_x, 230))
        screen.blit(info2, (panel_x, 270))
        screen.blit(info3, (panel_x, 310))
        screen.blit(info4, (panel_x, 350))

        # Pause button
        pause_hover = self.pause_button.collidepoint(mouse_pos)
        pause_color = (255, 200, 0) if pause_hover else (200, 150, 0)
        pause_text = "Resume" if self.controls.paused else "Pause"
        scale = 1.08 if pause_hover else 1.0
        
        if scale != 1.0:
            scaled_pause = pygame.Rect(
                self.pause_button.x - (self.pause_button.width * (scale - 1)) / 2,
                self.pause_button.y - (self.pause_button.height * (scale - 1)) / 2,
                self.pause_button.width * scale,
                self.pause_button.height * scale
            )
        else:
            scaled_pause = self.pause_button
        
        pygame.draw.rect(screen, pause_color, scaled_pause, border_radius=8)
        pause_surf = small_font.render(pause_text, True, (255, 255, 255))
        pause_rect = pause_surf.get_rect(center=scaled_pause.center)
        screen.blit(pause_surf, pause_rect)

        # Stop button
        stop_hover = self.stop_button.collidepoint(mouse_pos)
        stop_color = (255, 100, 100) if stop_hover else (200, 50, 50)
        scale = 1.08 if stop_hover else 1.0
        
        if scale != 1.0:
            scaled_stop = pygame.Rect(
                self.stop_button.x - (self.stop_button.width * (scale - 1)) / 2,
                self.stop_button.y - (self.stop_button.height * (scale - 1)) / 2,
                self.stop_button.width * scale,
                self.stop_button.height * scale
            )
        else:
            scaled_stop = self.stop_button
        
        pygame.draw.rect(screen, stop_color, scaled_stop, border_radius=8)
        stop_surf = small_font.render("Stop", True, (255, 255, 255))
        stop_rect = stop_surf.get_rect(center=scaled_stop.center)
        screen.blit(stop_surf, stop_rect)

        # Back button
        hover = self.back_button.collidepoint(mouse_pos)
        back_color = (255, 140, 0) if hover else (220, 120, 0)
        draw_button(screen, self.back_button, "Back", back_color, scale=get_button_scale(hover))

        # Pause text
        if self.controls.paused and not self.game_over:
            pause_text_display = title_font.render("PAUSED", True, (255, 200, 0))
            pause_text_rect = pause_text_display.get_rect(center=(self.grid_x + self.grid_width // 2, self.grid_y + self.grid_height // 2))
            screen.blit(pause_text_display, pause_text_rect)

        # Game Over text
        if self.game_over:
            caught_text = title_font.render("GREY CAUGHT!", True, (255, 0, 0))
            caught_rect = caught_text.get_rect(center=(self.grid_x + self.grid_width // 2, self.grid_y + self.grid_height // 2))
            screen.blit(caught_text, caught_rect)

        draw_exit_button(screen, self.exit_button, mouse_pos)