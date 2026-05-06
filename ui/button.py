import pygame
from ui.map import draw_grid, draw_agents, WIDTH, HEIGHT, GRID_AREA
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        # Colors (normal, hover, pressed)
        self.color_normal = (30, 100, 200)      # calm blue
        self.color_hover  = (60, 150, 240)      # brighter blue
        self.color_pressed = (20, 70, 160)      # darker blue when clicked
        self.shadow_offset = (3, 3)
        self.border_radius = 12
        self.hover = False
        self.clicked = False

    def update(self, mouse_pos, mouse_down):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hover and mouse_down

    def draw(self, screen, font):

        # ===== COLOR STATE =====
        if self.clicked:
            color = (0, 80, 180)      # click
        elif self.hover:
            pygame.draw.rect(screen, (255, 255, 255, 80), self.rect, width=2, border_radius=self.border_radius)     # normal
        else:
            color = (0, 120, 220)     # normal

        # ===== SHADOW =====
        shadow_rect = self.rect.move(self.shadow_offset)
        pygame.draw.rect(screen, (30, 30, 40), shadow_rect, border_radius=self.border_radius)

        # ===== BUTTON =====
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        # ===== TEXT =====
        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(
            txt,
            (self.rect.centerx - txt.get_width() // 2,
             self.rect.centery - txt.get_height() // 2)
        )

    def click(self, pos):
        return self.rect.collidepoint(pos)
class SimpleButton:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        # Colors (normal, hover, pressed)
        self.color_normal = (30, 100, 200)      # calm blue
        self.color_hover  = (60, 150, 240)      # brighter blue
        self.color_pressed = (20, 70, 160)      # darker blue when clicked
        self.shadow_offset = (3, 3)
        self.border_radius = 12

    def draw(self, screen, font):
        # Get current mouse state for visual feedback
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # left button
        hover = self.rect.collidepoint(mouse_pos)

        # Choose color based on state
        if hover and mouse_pressed:
            color = self.color_pressed
        elif hover:
            color = self.color_hover
        else:
            color = self.color_normal

        # Draw shadow
        shadow_rect = self.rect.move(self.shadow_offset)
        pygame.draw.rect(screen, (30, 30, 40), shadow_rect, border_radius=self.border_radius)

        # Draw main button
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        # Optional: subtle border when hovered
        if hover:
            pygame.draw.rect(screen, (255, 255, 255, 80), self.rect, width=2, border_radius=self.border_radius)

        # Draw text with slight drop shadow
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Text shadow (very subtle)
        shadow_text_rect = text_rect.move(1, 1)
        shadow_surf = font.render(self.text, True, (0, 0, 0, 100))
        screen.blit(shadow_surf, shadow_text_rect)
        screen.blit(text_surf, text_rect)

    def click(self, pos):
        return self.rect.collidepoint(pos)
pause_btn = SimpleButton(WIDTH - 180, 200, 140, 50, "PAUSE")
end_btn   = SimpleButton(WIDTH - 180, 300, 140, 50, "END")