import math
import pygame
from ui.effects import EffectsState, draw_animated_background, draw_particles, create_particle
from ui.components import title_font, small_font, draw_button, get_button_scale, draw_exit_button
from config import ScreenConfig

class StartScreen:
    def __init__(self):
        self.start_button = pygame.Rect(400, 350, 200, 70)
        self.exit_button = pygame.Rect(920, 20, 50, 50)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.collidepoint(event.pos):
                    return "QUIT"
                if self.start_button.collidepoint(event.pos):
                    EffectsState.particles.clear()
                    return "MENU"
        return None

    def update(self):
        pass

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        
        # Animated background
        draw_animated_background(screen, ScreenConfig.WIDTH, ScreenConfig.HEIGHT, EffectsState.animation_time * 2, EffectsState.animation_time)
        
        # Particles
        draw_particles(screen)
        if EffectsState.animation_time % 5 == 0:
            create_particle(mouse_pos[0], mouse_pos[1])

        # Overlay
        overlay = pygame.Surface((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((20, 40, 80))
        screen.blit(overlay, (0, 0))

        # Title animation
        title_y = 180 + math.sin(EffectsState.animation_time * 0.02) * 5
        title_text = title_font.render("Project AI Hust", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(ScreenConfig.WIDTH // 2, title_y))
        screen.blit(title_text, title_rect)

        subtitle_text = small_font.render("Click Start to continue", True, (230, 230, 230))
        subtitle_rect = subtitle_text.get_rect(center=(ScreenConfig.WIDTH // 2, 250))
        screen.blit(subtitle_text, subtitle_rect)

        hover = self.start_button.collidepoint(mouse_pos)
        start_color = (255, 140, 0) if hover else (220, 120, 0)
        scale = get_button_scale(hover)

        draw_button(screen, self.start_button, "Start", start_color, radius=12, scale=scale)
        draw_exit_button(screen, self.exit_button, mouse_pos)