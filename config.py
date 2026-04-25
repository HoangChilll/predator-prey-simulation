# =========================
# SCREEN CONFIG
# =========================
class ScreenConfig:
    WIDTH = 1000
    HEIGHT = 800
    FPS = 60
    TITLE = "Project AI Hust"


# =========================
# GRID CONFIG
# =========================
class GridConfig:
    WIDTH = 20
    HEIGHT = 20
    CELL_SIZE = 25

    @staticmethod
    def get_pixel_size():
        return (
            GridConfig.WIDTH * GridConfig.CELL_SIZE,
            GridConfig.HEIGHT * GridConfig.CELL_SIZE
        )


# =========================
# AGENT CONFIG
# =========================
class AgentConfig:
    NUM_PREDATORS = 1
    NUM_PREY = 1

    PREDATOR_SPEED = 1
    PREY_SPEED = 1


# =========================
# STRATEGY CONFIG (AI)
# =========================
class StrategyConfig:
    PREDATOR_STRATEGY = "astar"   # astar | bfs | greedy
    PREY_STRATEGY = "random"      # random | greedy


# =========================
# GAME RULE CONFIG
# =========================
class GameConfig:
    MAX_STEPS = 500
    CAPTURE_DISTANCE = 0   # 0 = cùng ô là bắt
    SIMULATION_FPS = 2     # Tốc độ chạy thuật toán (bước/giây)
    TURN_BASED = True


# =========================
# UI CONFIG
# =========================
class UIConfig:
    SHOW_GRID = True
    SHOW_PATH = False
    SHOW_COORDS = False


# =========================
# COLOR CONFIG
# =========================
class ColorConfig:
    BACKGROUND = (30, 30, 30)
    GRID = (60, 60, 60)

    PREDATOR = (255, 80, 80)
    PREY = (80, 255, 80)

    # Grid Colors
    EMPTY_CELL = (240, 240, 240)
    WALL = (50, 50, 50)
    GRID_BORDER = (200, 200, 200)

    TEXT = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 200)
    TEXT_HINT = (180, 180, 180)
    TEXT_ACCENT = (255, 255, 0)
    TEXT_PREDATOR = (255, 150, 150)
    TEXT_PREY = (150, 255, 150)

    # UI Colors
    GAME_BACKGROUND = (0, 0, 0)
    MENU_BACKGROUND = (30, 100, 130)
    GAME_OVER_BACKGROUND = (0, 0, 0)

    # Menu Screen
    MENU_BUTTON_GRID = (50, 120, 140)
    MENU_BUTTON_PREDATOR = (140, 70, 70)
    MENU_BUTTON_PREY = (70, 140, 70)
    MENU_BUTTON_START = (200, 180, 50)
    MENU_BUTTON_BORDER = (255, 255, 255)
    MENU_HINT = (230, 230, 230)

    # Pause Screen
    PAUSE_OVERLAY = (0, 0, 0, 160)
    PAUSE_WINDOW = (40, 40, 40)
    PAUSE_BUTTON = (80, 160, 240)
    PAUSE_BUTTON_BORDER = (255, 255, 255)
    PAUSE_TITLE = (255, 80, 80)
class ControlConfig:
    KEY_PAUSE = "p"
    KEY_STEP = "n"
    KEY_RESET = "r"