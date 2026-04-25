import pygame
from ui.screens.base_screen import BaseScreen
from config import ColorConfig

class PauseScreen(BaseScreen):
    def __init__(self, game_screen):
        self.game_screen = game_screen
        self.button_rect = pygame.Rect(300, 320, 200, 60)
        self.title_font = pygame.font.SysFont(None, 64)
        self.text_font = pygame.font.SysFont(None, 32)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    return ("RESUME", self.game_screen)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_RETURN):
                    return ("RESUME", self.game_screen)
                if event.key == pygame.K_ESCAPE:
                    return ("MENU", None)

        return None

    def update(self):
        return None

    def draw(self, screen):
        self.game_screen.draw(screen)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(ColorConfig.PAUSE_OVERLAY)
        screen.blit(overlay, (0, 0))

        window_rect = pygame.Rect(200, 180, 400, 240)
        pygame.draw.rect(screen, ColorConfig.PAUSE_WINDOW, window_rect)
        pygame.draw.rect(screen, ColorConfig.PAUSE_BUTTON_BORDER, window_rect, 3)

        title = self.title_font.render("Paused", True, ColorConfig.PAUSE_TITLE)
        text = self.text_font.render("Game is paused.", True, ColorConfig.TEXT_SECONDARY)
        hint = self.text_font.render("Press Continue or P to resume", True, ColorConfig.TEXT_HINT)
        button_text = self.text_font.render("Continue", True, ColorConfig.TEXT)

        title_rect = title.get_rect(center=(window_rect.centerx, window_rect.top + 50))
        text_rect = text.get_rect(center=(window_rect.centerx, window_rect.top + 120))
        hint_rect = hint.get_rect(center=(window_rect.centerx, window_rect.top + 160))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)

        pygame.draw.rect(screen, ColorConfig.PAUSE_BUTTON, self.button_rect)
        pygame.draw.rect(screen, ColorConfig.PAUSE_BUTTON_BORDER, self.button_rect, 2)

        screen.blit(title, title_rect)
        screen.blit(text, text_rect)
        screen.blit(hint, hint_rect)
        screen.blit(button_text, button_text_rect)
