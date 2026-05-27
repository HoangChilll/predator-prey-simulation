import pygame
from ui.button import Button

from ui.constants import WIDTH, HEIGHT, log
from ui.grid import grid10x10,grid20x20_2 ,MAZE_20,grid20x20, grid40x40,grid40x40_2
from ui.dropdown import Dropdown, toggle_dropdown, update_dropdown


MATRICES = {
    "10_1": grid10x10,
    "20_2": grid20x20_2,
    "20": MAZE_20,
    "20_1": grid20x20,
    "40": grid40x40,
    "40_2": grid40x40_2

    
 
}

def selectMatrix(name):
    if name not in MATRICES:
        raise ValueError(f"Matrix '{name}' không tồn tại")
    
    return MATRICES[name]



def get_config():
    cfg = {
        "grid": "10_1",
        "prey_algo": "random",
        "grey_algo": "greedy"
    }
    log(f"INIT CONFIG: {cfg}")
    return cfg



# UI RENDER

def draw_config(screen, font, buttons, dropdowns):
    for y in range(HEIGHT):
        # màu 
        ratio = y / HEIGHT
        r = int(255 * (1 - ratio) + 245 * ratio)      # 255 -> 245
        g = int(180 * (1 - ratio) + 210 * ratio)      # 180 -> 210
        b = int(50  * (1 - ratio) + 100 * ratio)      # 50  -> 100
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    # 2. vẽ panel 
    panel_margin = 40
    panel_rect = pygame.Rect(panel_margin, panel_margin,
                             WIDTH - 2*panel_margin, HEIGHT - 2*panel_margin)
    panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel_surface, (30, 30, 40, 180), panel_surface.get_rect(), border_radius=20)
    pygame.draw.rect(panel_surface, (200, 180, 100, 255), panel_surface.get_rect(), width=2, border_radius=20)
    screen.blit(panel_surface, (panel_margin, panel_margin))

    # 3. vẽ tiêu đề đổ bóng
    title_text = "CONFIGURATION"
    # đổ bóng
    shadow_surf = font.render(title_text, True, (0, 0, 0, 100))
    shadow_rect = shadow_surf.get_rect(center=(WIDTH//2 + 4, int(HEIGHT*0.1) + 4))
    screen.blit(shadow_surf, shadow_rect)
    

    # vẽ tiêu đề
    title = font.render(title_text, True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.1)))
    screen.blit(title, title_rect)

    line_y = title_rect.bottom + 10
    line_width = 150
    pygame.draw.line(screen, (255, 220, 150), (WIDTH//2 - line_width//2, line_y),
                     (WIDTH//2 + line_width//2, line_y), 3)

    # vẽ nút
    for btn in buttons:
        btn.draw(screen, font)

    # vẽ list
    for dd in dropdowns.values():
        dd.draw(screen, font)

    pygame.display.flip()



#hàm xử lý input
def handle_config_click(pos, buttons, dropdowns, config):

   
    for btn in buttons:

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        btn.update(mouse_pos, mouse_down)

        if btn.click(pos):

            log(f"CLICK BUTTON: {btn.text}")

            
            if btn.text == "PREY":
                toggle_dropdown(dropdowns, "prey")

            
            elif btn.text == "GREY":
                toggle_dropdown(dropdowns, "grey")

            
            elif btn.text == "GRID":
                toggle_dropdown(dropdowns, "grid")

           
            elif btn.text == "START":

                config["matrix"] = selectMatrix(config["grid"])

                log(f"START GAME WITH CONFIG: {config}")

                return "START"

    

    update_dropdown(config, dropdowns, "prey", "prey_algo")

    update_dropdown(config, dropdowns, "grey", "grey_algo")

    update_dropdown(config, dropdowns, "grid", "grid")

    return None





def create_ui():
    btn_width = 120
    btn_height = 40
    btn_spacing = 20
    total_btn_width = 4 * btn_width + 3 * btn_spacing
    start_x = (WIDTH - total_btn_width) // 2
    btn_y = int(HEIGHT * 0.25)
    buttons = []
    btn_texts = ["PREY", "GREY", "GRID", "START"]
    for i, text in enumerate(btn_texts):
        x = start_x + i * (btn_width + btn_spacing)
        buttons.append(Button(x, btn_y, btn_width, btn_height, text))
    dropdowns = {
        "prey": Dropdown(["random", "p_dfs","p_greedy", "p_A*", "huy_minimax_prey"], buttons[0].rect.x, buttons[0].rect.y + btn_height + 5),
        "grey": Dropdown([ "g_dfs","random","g_greedy", "huy_minimax_grey", "grey_A*"], buttons[1].rect.x, buttons[1].rect.y + btn_height + 5),
        "grid": Dropdown(["10_1", "20_2", "20_1","20", "40", "40_2"], buttons[2].rect.x, buttons[2].rect.y + btn_height + 5),
    }
    log("UI CREATED (buttons + dropdowns)")
    return buttons, dropdowns 