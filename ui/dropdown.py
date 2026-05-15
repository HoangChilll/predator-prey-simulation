import pygame
from ui.constants import log

def toggle_dropdown(dropdowns, key):

    if key not in dropdowns:
        log(f"Dropdown '{key}' không tồn tại")
        return

    for k in dropdowns:
        dropdowns[k].visible = (k == key and not dropdowns[k].visible)

    log(f"DROPDOWN STATE: {key} -> {dropdowns[key].visible}")
def update_dropdown(config, dropdowns, key, config_key):
    value = dropdowns[key].handle_click(pygame.mouse.get_pos())

    if value is not None:
        config[config_key] = value
        dropdowns[key].selected = value
        dropdowns[key].visible = False

        log(f"SELECT {config_key} = {value}")
        log(f"CONFIG UPDATE: {config}")
# DROPDOWN

class Dropdown:
    def __init__(self, options, x, y):
        self.options = options
        self.visible = False
        self.selected = options[0]

        self.rects = []
        for i, opt in enumerate(options):
            self.rects.append((pygame.Rect(x, y + i * 35, 120, 30), opt))

    def draw(self, screen, font):
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()

        for i, (rect, opt) in enumerate(self.rects):
            # Determine background colour
            if rect.collidepoint(mouse_pos):
                bg_color = (100, 100, 130)       # hover
            elif opt == self.selected:
                bg_color = (60, 80, 120)         # selected option
            else:
                bg_color = (50, 50, 65)          # normal

            # Draw rounded rectangle
            pygame.draw.rect(screen, bg_color, rect, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 210), rect, width=2, border_radius=6)

            # Render text
            text_surf = font.render(str(opt), True, (255, 255, 255))
            text_x = rect.x + 10
            text_y = rect.y + (rect.height - text_surf.get_height()) // 2
            screen.blit(text_surf, (text_x, text_y))

    def handle_click(self, pos):
        if not self.visible:
            return None

        for rect, opt in self.rects:
            if rect.collidepoint(pos):
                self.selected = opt
                self.visible = False

                log(f"DROPDOWN SELECT: {opt}")
                return opt

        return None

