import math
import pygame
from ui.effects import EffectsState, draw_animated_background, draw_particles, create_particle
from ui.components import title_font, button_font, small_font, draw_button, draw_exit_button
from config import ScreenConfig

class MenuScreen:
    def __init__(self):
        # State
        self.selected_size = None
        self.selected_predator_algo = None
        self.selected_prey_algo = None
        self.has_saved_matrix = False
        self.last_size = None
        self.last_predator_algo = None
        self.last_prey_algo = None

        # Buttons
        self.back_button = pygame.Rect(40, 40, 140, 55)
        self.exit_button = pygame.Rect(920, 20, 50, 50)
        self.simulate_button = pygame.Rect(400, 600, 200, 70)
        self.reuse_button = pygame.Rect(200, 600, 240, 70)
        self.new_button = pygame.Rect(560, 600, 240, 70)

        self.size_buttons = [
            ("5x5", pygame.Rect(220, 230, 110, 55)),
            ("10x10", pygame.Rect(380, 230, 110, 55)),
            ("15x15", pygame.Rect(540, 230, 110, 55)),
            ("20x20", pygame.Rect(700, 230, 110, 55)),
        ]
        
        self.predator_algo_buttons = [
            ("BFS", pygame.Rect(220, 360, 110, 55)),
            ("DFS", pygame.Rect(380, 360, 110, 55)),
            ("A*", pygame.Rect(540, 360, 110, 55)),
        ]
        
        self.prey_algo_buttons = [
            ("BFS", pygame.Rect(220, 460, 110, 55)),
            ("DFS", pygame.Rect(380, 460, 110, 55)),
            ("A*", pygame.Rect(540, 460, 110, 55)),
        ]

    def _map_algo_to_config(self, text):
        if text == "BFS": return "bfs"
        if text == "DFS": return "dfs"
        return "astar"

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
                    self.selected_size = None
                    self.selected_predator_algo = None
                    self.selected_prey_algo = None
                    return "START"

                for text, rect in self.size_buttons:
                    if rect.collidepoint(event.pos):
                        self.selected_size = text

                for text, rect in self.predator_algo_buttons:
                    if rect.collidepoint(event.pos):
                        self.selected_predator_algo = text
                        
                for text, rect in self.prey_algo_buttons:
                    if rect.collidepoint(event.pos):
                        self.selected_prey_algo = text

                if not self.has_saved_matrix and self.simulate_button.collidepoint(event.pos):
                    if self.selected_size and self.selected_predator_algo and self.selected_prey_algo:
                        self.last_size = self.selected_size
                        self.last_predator_algo = self.selected_predator_algo
                        self.last_prey_algo = self.selected_prey_algo
                        self.has_saved_matrix = True
                        
                        grid_val = int(self.selected_size.split('x')[0])
                        config = {
                            "grid_size": grid_val,
                            "predator_strategy": self._map_algo_to_config(self.selected_predator_algo),
                            "prey_strategy": self._map_algo_to_config(self.selected_prey_algo)
                        }
                        return ("GAME", config)

                if self.has_saved_matrix and self.reuse_button.collidepoint(event.pos):
                    grid_val = int(self.last_size.split('x')[0])
                    config = {
                        "grid_size": grid_val,
                        "predator_strategy": self._map_algo_to_config(self.last_predator_algo),
                        "prey_strategy": self._map_algo_to_config(self.last_prey_algo)
                    }
                    return ("GAME", config)

                if self.has_saved_matrix and self.new_button.collidepoint(event.pos):
                    self.has_saved_matrix = False
                    self.selected_size = None
                    self.selected_predator_algo = None
                    self.selected_prey_algo = None
                    self.last_size = None
                    self.last_predator_algo = None
                    self.last_prey_algo = None

        return None

    def update(self):
        pass

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        
        draw_animated_background(screen, ScreenConfig.WIDTH, ScreenConfig.HEIGHT, EffectsState.animation_time * 2, EffectsState.animation_time)
        draw_particles(screen)
        
        if EffectsState.animation_time % 5 == 0:
            create_particle(mouse_pos[0], mouse_pos[1])

        overlay = pygame.Surface((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((20, 40, 80))
        screen.blit(overlay, (0, 0))

        title_y = 110 + math.sin(EffectsState.animation_time * 0.02) * 5
        title_text = title_font.render("Setup", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(ScreenConfig.WIDTH // 2, title_y))
        screen.blit(title_text, title_rect)

        size_label = button_font.render("Select Matrix Size", True, (255, 255, 255))
        screen.blit(size_label, (220, 180))

        for i, (text, rect) in enumerate(self.size_buttons):
            if text == self.selected_size:
                color = (0, 180, 0)
            elif rect.collidepoint(mouse_pos):
                color = (255, 140, 0)
            else:
                color = (220, 120, 0)

            bounce = math.sin(EffectsState.animation_time * 0.03 + i * 0.3) * 3
            animated_rect = pygame.Rect(rect.x, rect.y + bounce, rect.width, rect.height)
            
            scale = 1.08 if rect.collidepoint(mouse_pos) or text == self.selected_size else 1.0
            
            if scale != 1.0:
                scaled_rect = pygame.Rect(
                    animated_rect.x - (animated_rect.width * (scale - 1)) / 2,
                    animated_rect.y - (animated_rect.height * (scale - 1)) / 2,
                    animated_rect.width * scale,
                    animated_rect.height * scale
                )
            else:
                scaled_rect = animated_rect
            
            pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
            text_surface = button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=scaled_rect.center)
            screen.blit(text_surface, text_rect)

        predator_label = button_font.render("Predator Algorithm", True, (255, 255, 255))
        screen.blit(predator_label, (220, 310))

        for i, (text, rect) in enumerate(self.predator_algo_buttons):
            if text == self.selected_predator_algo:
                color = (255, 50, 50)  # Red for predator
            elif rect.collidepoint(mouse_pos):
                color = (255, 100, 100)
            else:
                color = (200, 50, 50)

            bounce = math.sin(EffectsState.animation_time * 0.03 + i * 0.3) * 3
            animated_rect = pygame.Rect(rect.x, rect.y + bounce, rect.width, rect.height)
            
            scale = 1.08 if rect.collidepoint(mouse_pos) or text == self.selected_predator_algo else 1.0
            
            if scale != 1.0:
                scaled_rect = pygame.Rect(
                    animated_rect.x - (animated_rect.width * (scale - 1)) / 2,
                    animated_rect.y - (animated_rect.height * (scale - 1)) / 2,
                    animated_rect.width * scale,
                    animated_rect.height * scale
                )
            else:
                scaled_rect = animated_rect
            
            pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
            text_surface = button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=scaled_rect.center)
            screen.blit(text_surface, text_rect)

        prey_label = button_font.render("Prey Algorithm", True, (255, 255, 255))
        screen.blit(prey_label, (220, 420))

        for i, (text, rect) in enumerate(self.prey_algo_buttons):
            if text == self.selected_prey_algo:
                color = (50, 200, 50)  # Green for prey
            elif rect.collidepoint(mouse_pos):
                color = (100, 255, 100)
            else:
                color = (50, 150, 50)

            bounce = math.sin(EffectsState.animation_time * 0.03 + i * 0.3) * 3
            animated_rect = pygame.Rect(rect.x, rect.y + bounce, rect.width, rect.height)
            
            scale = 1.08 if rect.collidepoint(mouse_pos) or text == self.selected_prey_algo else 1.0
            
            if scale != 1.0:
                scaled_rect = pygame.Rect(
                    animated_rect.x - (animated_rect.width * (scale - 1)) / 2,
                    animated_rect.y - (animated_rect.height * (scale - 1)) / 2,
                    animated_rect.width * scale,
                    animated_rect.height * scale
                )
            else:
                scaled_rect = animated_rect
            
            pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
            text_surface = button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=scaled_rect.center)
            screen.blit(text_surface, text_rect)

        info_size = small_font.render(f"Size: {self.selected_size}", True, (255, 255, 255))
        info_predator = small_font.render(f"Predator: {self.selected_predator_algo}", True, (255, 150, 150))
        info_prey = small_font.render(f"Prey: {self.selected_prey_algo}", True, (150, 255, 150))
        
        screen.blit(info_size, (750, 310))
        screen.blit(info_predator, (750, 350))
        screen.blit(info_prey, (750, 390))

        if not self.has_saved_matrix:
            if self.selected_size and self.selected_predator_algo and self.selected_prey_algo:
                if self.simulate_button.collidepoint(mouse_pos):
                    sim_color = (0, 220, 0)
                else:
                    sim_color = (0, 180, 0)
                scale = 1.1 if self.simulate_button.collidepoint(mouse_pos) else 1.0
            else:
                sim_color = (120, 120, 120)
                scale = 1.0

            draw_button(screen, self.simulate_button, "Simulate", sim_color, radius=12, scale=scale)
        
        if self.has_saved_matrix:
            reuse_hover = self.reuse_button.collidepoint(mouse_pos)
            reuse_color = (100, 200, 100) if reuse_hover else (50, 150, 50)
            scale = 1.08 if reuse_hover else 1.0
            reuse_text = f"Reuse: {self.last_size} {self.last_predator_algo}/{self.last_prey_algo}"
            draw_button(screen, self.reuse_button, reuse_text, reuse_color, radius=12, scale=scale)
            
            new_hover = self.new_button.collidepoint(mouse_pos)
            new_color = (100, 180, 255) if new_hover else (50, 120, 200)
            scale = 1.08 if new_hover else 1.0
            draw_button(screen, self.new_button, "New Setup", new_color, radius=12, scale=scale)

        hover = self.back_button.collidepoint(mouse_pos)
        back_color = (255, 140, 0) if hover else (220, 120, 0)
        draw_button(screen, self.back_button, "Back", back_color, scale=1.1 if hover else 1.0)

        draw_exit_button(screen, self.exit_button, mouse_pos)