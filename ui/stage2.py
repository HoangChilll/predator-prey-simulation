import pygame
from log import log
from ui.button import Button
WIDTH = 800
HEIGHT = 600

# CONFIG FACTORY
#prey :mồi, predator :grey thú
def get_config():
    cfg = {
        "size": 10,
        "prey_algo": "random",
        "grey_algo": "greedy"
    }
    log(f"INIT CONFIG: {cfg}")
    return cfg



# UI RENDER

def draw_config(screen, font, buttons, dropdowns):
    screen.fill((255, 180, 50))

    title = font.render("CONFIGURATION", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.1)))
    screen.blit(title, title_rect)

    for btn in buttons:
        btn.draw(screen, font)

    for dd in dropdowns.values():
        dd.draw(screen, font)

    pygame.display.flip()



# INPUT HANDLER

def handle_config_click(pos, buttons, dropdowns, config):
    
    # ===== BUTTON CLICK =====
    for btn in buttons:
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        btn.update(mouse_pos, mouse_down)
        if btn.click(pos):

            log(f"CLICK BUTTON: {btn.text}")

            if btn.text == "PREY":
                log("TOGGLE DROPDOWN: PREY")
                toggle_dropdown(dropdowns, "prey")

            elif btn.text == "GREY":
                log("TOGGLE DROPDOWN: GREY")
                toggle_dropdown(dropdowns, "grey")

            elif btn.text == "SIZE":
                log("TOGGLE DROPDOWN: SIZE")
                toggle_dropdown(dropdowns, "size")

            elif btn.text == "START":
                log(f"START GAME WITH CONFIG: {config}")
                return "START"

    # ===== DROPDOWN SELECT =====
    update_dropdown(config, dropdowns, "prey", "prey_algo")
    update_dropdown(config, dropdowns, "grey", "grey_algo")
    update_dropdown(config, dropdowns, "size", "size", is_int=True)

    return None



# HELPERS

def toggle_dropdown(dropdowns, key):
    for k in dropdowns:
        dropdowns[k].visible = (k == key and not dropdowns[k].visible)

    log(f"DROPDOWN STATE: {key} -> {dropdowns[key].visible}")


def update_dropdown(config, dropdowns, key, config_key, is_int=False):
    value = dropdowns[key].handle_click(pygame.mouse.get_pos())

    if value is not None:
        config[config_key] = int(value) if is_int else value
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

        for rect, opt in self.rects:
            pygame.draw.rect(screen, (80, 80, 80), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)  # viền sáng
            txt = font.render(str(opt), True, (255, 255, 255))
            screen.blit(txt, (rect.x + 5, rect.y + 5))

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


# UI INIT

def create_ui():
    btn_width = 120
    btn_height = 40
    btn_spacing = 20
    total_btn_width = 4 * btn_width + 3 * btn_spacing
    start_x = (WIDTH - total_btn_width) // 2
    btn_y = int(HEIGHT * 0.25)
    buttons = []
    btn_texts = ["PREY", "GREY", "SIZE", "START"]
    for i, text in enumerate(btn_texts):
        x = start_x + i * (btn_width + btn_spacing)
        buttons.append(Button(x, btn_y, btn_width, btn_height, text))
    dropdowns = {
        "prey": Dropdown(["random", "predator_dfs","predator_greedy"], buttons[0].rect.x, buttons[0].rect.y + btn_height + 5),
        "grey": Dropdown(["greedy", "prey_dfs","random","prey_greedy"], buttons[1].rect.x, buttons[1].rect.y + btn_height + 5),
        "size": Dropdown([10, 20, 30, 40, 50], buttons[2].rect.x, buttons[2].rect.y + btn_height + 5),
    }
    log("UI CREATED (buttons + dropdowns)")
    return buttons, dropdowns 