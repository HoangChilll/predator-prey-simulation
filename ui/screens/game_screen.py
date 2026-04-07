import pygame
from ui.controls import GameControls
from ui.screens.base_screen import BaseScreen
from core.maps import get_random_map
from simulation.simulator import Simulator
from core.grid import Grid
from ui.render import Renderer
from agents.strategies.strategie_factory import get_predator_strategy, get_prey_strategy
from config import ColorConfig

class GameScreen(BaseScreen):
    def __init__(self, config):
        super().__init__()

        # ===== CONFIG =====
        self.grid_size = config["grid_size"]
        self.predator_strategy = get_predator_strategy(config["predator_strategy"])
        self.prey_strategy = get_prey_strategy(config["prey_strategy"])

        # ===== TẠO GRID =====
        self.grid = Grid(self.grid_size, self.grid_size)

        # 🔥 LOAD MAP RANDOM
        map_data = get_random_map(self.grid_size)
        self.grid.load_map(map_data)

        # ===== SIMULATOR =====
        self.simulator = Simulator(
            self.grid,
            self.predator_strategy,
            self.prey_strategy
        )

        # ===== SPAWN AGENTS =====
        self.simulator.add_predator(0, 0)
        self.simulator.add_prey(self.grid_size - 1, self.grid_size - 1)

        # ===== RENDER =====
        self.renderer = Renderer(
            self.grid,
            self.grid_size,
            40   # cell_size (pixel mỗi ô)
        )

        # ===== STATE =====
        self.controls = GameControls(config)

    # =========================
    # EVENT
    # =========================
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.controls.paused = True
                return ("PAUSE", self)

        control_result = self.controls.handle_events(events)
        if control_result:
            return control_result

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return ("MENU", None)

        return None

    # =========================
    # UPDATE
    # =========================
    def update(self):
        return self.controls.update(self.simulator)

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        screen.fill(ColorConfig.GAME_BACKGROUND)

        # ===== TÍNH CELL SIZE =====
        cell_size = 600 // self.grid_size

        # vẽ grid
        self.renderer = Renderer(
            self.grid,
            self.simulator,
            cell_size
        )
        self.renderer.draw(screen)

        # hiển thị info
        font = pygame.font.SysFont(None, 30)

        text1 = font.render(f"Grid: {self.grid_size}x{self.grid_size}", True, ColorConfig.TEXT)
        text2 = font.render(f"Predator: {self.predator_strategy.name}", True, ColorConfig.TEXT_PREDATOR)
        text3 = font.render(f"Prey: {self.prey_strategy.name}", True, ColorConfig.TEXT_PREY)
        text4 = font.render(self.controls.get_control_hint(), True, ColorConfig.TEXT_ACCENT)
        text5 = font.render(f"Status: {self.controls.get_status_label()}", True, ColorConfig.TEXT)
        text6 = font.render(f"Predator Steps: {self.simulator.predator_steps}", True, ColorConfig.TEXT)

        # 🔥 THÊM: căn phải
        def draw_right(text, y):
            rect = text.get_rect()
            rect.topright = (screen.get_width() - 10, y)
            screen.blit(text, rect)

        draw_right(text1, 10)
        draw_right(text2, 40)
        draw_right(text3, 70)
        draw_right(text4, 100)
        draw_right(text5, 130)
        draw_right(text6, 160)