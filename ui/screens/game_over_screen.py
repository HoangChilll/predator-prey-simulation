import pygame
from ui.screens.base_screen import BaseScreen
from config import ColorConfig

class GameOverScreen(BaseScreen):
    def __init__(self, result):
        self.result = result
        self.title_font = pygame.font.SysFont(None, 64)
        self.text_font = pygame.font.SysFont(None, 32)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                return "MENU"

    def draw(self, screen):
        screen.fill(ColorConfig.GAME_OVER_BACKGROUND)

        title = self.title_font.render("Game Over", True, ColorConfig.PAUSE_TITLE)
        subtitle = self.text_font.render(self.result["message"], True, ColorConfig.TEXT)
        steps_text = self.text_font.render(f"Predator Steps: {self.result['predator_steps']}", True, ColorConfig.TEXT_SECONDARY)
        info = self.text_font.render("Press any key to return to Menu", True, ColorConfig.TEXT_HINT)

        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        steps_rect = steps_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        info_rect = info.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        screen.blit(steps_text, steps_rect)
        screen.blit(info, info_rect)
