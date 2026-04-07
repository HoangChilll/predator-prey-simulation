import pygame
from ui.screens.base_screen import BaseScreen

class StartScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        # màu
        self.bg_color = (30, 100, 130)
        self.button_color = (240, 120, 50)
        self.button_hover_color = (255, 150, 80)
        self.text_color = (0, 0, 0)

        # font
        self.font = pygame.font.SysFont(None, 30)

        # nút (ở giữa màn hình)
        self.button_rect = pygame.Rect(0, 0, 150, 50)
        self.button_rect.center = (400, 300)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(mouse_pos):
                    return "MENU"  # chuyển sang menu

        return None

    def update(self):
        pass

    def draw(self, screen):
        # nền
        screen.fill(self.bg_color)

        # hover effect
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            color = self.button_hover_color
        else:
            color = self.button_color

        # vẽ nút
        pygame.draw.rect(screen, color, self.button_rect)

        # text "Bắt đầu"
        text_surface = self.font.render("START", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.button_rect.center)

        screen.blit(text_surface, text_rect)