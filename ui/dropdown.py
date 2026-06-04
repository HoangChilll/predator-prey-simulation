import pygame
from ui.constants import log

_FONTS = {}


def _f(size):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("Arial", size)
    return _FONTS[size]


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


class Dropdown:
    def __init__(self, options, x, y):
        self.options = options
        self.visible = False
        self.selected = options[0]
        self.rects = []
        for i, opt in enumerate(options):
            self.rects.append((pygame.Rect(x, y + i * 34, 138, 32), opt))

    def draw(self, screen, font):
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        n = len(self.rects)

        # Drop-shadow for entire menu block
        if self.rects:
            total_h = n * 34 + 4
            fr = self.rects[0][0]
            shadow = pygame.Rect(fr.x + 4, fr.y + 4, fr.width, total_h)
            pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=8)

        for i, (rect, opt) in enumerate(self.rects):
            is_sel   = (opt == self.selected)
            is_hover = rect.collidepoint(mouse_pos)

            if is_hover:
                bg = (55, 90, 172)
            elif is_sel:
                bg = (35, 65, 142)
            else:
                bg = (20, 24, 44)

            r = 8 if (i == 0 or i == n - 1) else 4
            pygame.draw.rect(screen, bg, rect, border_radius=r)
            border_col = (90, 130, 222) if is_sel else (48, 68, 118)
            pygame.draw.rect(screen, border_col, rect, width=1, border_radius=r)

            # Gold dot for selected item
            if is_sel:
                pygame.draw.circle(screen, (255, 200, 50), (rect.x + 11, rect.centery), 4)
                tx = rect.x + 22
            else:
                tx = rect.x + 11

            ts = _f(20).render(str(opt), True, (222, 228, 248))
            screen.blit(ts, (tx, rect.y + (rect.height - ts.get_height()) // 2))

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
