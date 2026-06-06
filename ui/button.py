import pygame
from ui.constants import WIDTH, GRID_AREA


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.border_radius = 10
        self.shadow_offset = (3, 3)
        self.hover = False
        self.clicked = False

    def update(self, mouse_pos, mouse_down):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hover and mouse_down

    def draw(self, screen, font):
        if self.clicked:
            color  = (18, 68, 168)
            border = (100, 150, 255)
        elif self.hover:
            color  = (50, 130, 240)
            border = (140, 190, 255)
        else:
            color  = (28, 98, 210)
            border = (75, 130, 200)

        # Shadow
        pygame.draw.rect(screen, (0, 0, 0),
                         self.rect.move(self.shadow_offset),
                         border_radius=self.border_radius)
        # Body
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        # Top sheen
        sheen = pygame.Surface((self.rect.width - 8, self.rect.height // 2 - 2),
                               pygame.SRCALPHA)
        sheen.fill((255, 255, 255, 20))
        screen.blit(sheen, (self.rect.x + 4, self.rect.y + 3))
        # Border
        pygame.draw.rect(screen, border, self.rect,
                         width=2, border_radius=self.border_radius)
        # Text
        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, pos):
        return self.rect.collidepoint(pos)


class SimpleButton:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.border_radius = 10

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        pressed = hover and pygame.mouse.get_pressed()[0]

        if pressed:
            color  = (18, 68, 168)
            border = (100, 150, 255)
        elif hover:
            color  = (50, 130, 240)
            border = (140, 190, 255)
        else:
            color  = (28, 98, 210)
            border = (75, 130, 200)

        pygame.draw.rect(screen, (0, 0, 0),
                         self.rect.move(3, 3), border_radius=self.border_radius)
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        sheen = pygame.Surface((self.rect.width - 8, self.rect.height // 2 - 2),
                               pygame.SRCALPHA)
        sheen.fill((255, 255, 255, 20))
        screen.blit(sheen, (self.rect.x + 4, self.rect.y + 3))
        pygame.draw.rect(screen, border, self.rect,
                         width=2, border_radius=self.border_radius)
        ts = font.render(self.text, True, (255, 255, 255))
        screen.blit(ts, ts.get_rect(center=self.rect.center))

    def click(self, pos):
        return self.rect.collidepoint(pos)


# Positioned inside the right-side HUD panel (x=GRID_AREA..WIDTH)
_bx = GRID_AREA + 25   # 625
pause_btn = SimpleButton(_bx, 410, 150, 44, "PAUSE")
end_btn   = SimpleButton(_bx, 468, 150, 44, "END")
