import pygame
from ui.screens.base_screen import BaseScreen
from config import ColorConfig

class MenuScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        # ===== DATA =====
        self.grid_sizes = [5, 10, 15, 20, 25]
        self.grid_index = 1  # mặc định 10x10

        self.strategies = ["bfs", "dfs", "astar"]
        self.predator_index = 0
        self.prey_index = 0

        # ===== UI =====
        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)

        self.grid_button_rect = pygame.Rect(100, 150, 360, 60)
        self.predator_button_rect = pygame.Rect(100, 230, 360, 60)
        self.prey_button_rect = pygame.Rect(100, 310, 360, 60)
        self.start_button_rect = pygame.Rect(100, 390, 360, 70)

    # =========================
    # EVENT
    # =========================
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.grid_button_rect.collidepoint(event.pos):
                    self.grid_index = (self.grid_index + 1) % len(self.grid_sizes)

                elif self.predator_button_rect.collidepoint(event.pos):
                    self.predator_index = (self.predator_index + 1) % len(self.strategies)

                elif self.prey_button_rect.collidepoint(event.pos):
                    self.prey_index = (self.prey_index + 1) % len(self.strategies)

                elif self.start_button_rect.collidepoint(event.pos):
                    config = {
                        "grid_size": self.grid_sizes[self.grid_index],
                        "predator_strategy": self.strategies[self.predator_index],
                        "prey_strategy": self.strategies[self.prey_index]
                    }
                    return ("GAME", config)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    config = {
                        "grid_size": self.grid_sizes[self.grid_index],
                        "predator_strategy": self.strategies[self.predator_index],
                        "prey_strategy": self.strategies[self.prey_index]
                    }
                    return ("GAME", config)

        return None

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        screen.fill(ColorConfig.MENU_BACKGROUND)

        grid_size = self.grid_sizes[self.grid_index]
        predator = self.strategies[self.predator_index]
        prey = self.strategies[self.prey_index]

        title = self.title_font.render("PREDATOR - PREY SIMULATION", True, (255, 255, 255))
        screen.blit(title, (50, 50))

        def draw_button(rect, text, bg_color, border_color):
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, 3)
            text_surf = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        draw_button(
            self.grid_button_rect,
            f"Map Size: {grid_size}x{grid_size}",
            ColorConfig.MENU_BUTTON_GRID,
            ColorConfig.MENU_BUTTON_BORDER
        )

        draw_button(
            self.predator_button_rect,
            f"Predator Strategy: {predator}",
            ColorConfig.MENU_BUTTON_PREDATOR,
            ColorConfig.MENU_BUTTON_BORDER
        )

        draw_button(
            self.prey_button_rect,
            f"Prey Strategy: {prey}",
            ColorConfig.MENU_BUTTON_PREY,
            ColorConfig.MENU_BUTTON_BORDER
        )

        draw_button(
            self.start_button_rect,
            "Start Simulation",
            ColorConfig.MENU_BUTTON_START,
            ColorConfig.MENU_BUTTON_BORDER
        )

        hint = self.font.render("Click a button to change selection", True, ColorConfig.MENU_HINT)
        screen.blit(hint, (100, 470))