import pygame
from ui.screens.start_screen import StartScreen
from ui.screens.menu_screen import MenuScreen
from ui.screens.game_screen import GameScreen
from ui.screens.pause_screen import PauseScreen
from ui.screens.game_over_screen import GameOverScreen
from config import ScreenConfig

def main():
    pygame.init()
    screen = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
    pygame.display.set_caption(ScreenConfig.TITLE)
    clock = pygame.time.Clock()

    screens = {
        "START": StartScreen(),
        "MENU": MenuScreen(),
    }

    current_screen = screens["START"]

    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # --- input ---
        result = current_screen.handle_events(events)

        # 🔥 xử lý chuyển màn hình
        if result == "MENU":
            current_screen = screens["MENU"]

        elif isinstance(result, tuple):
            screen_name, config = result

            if screen_name == "GAME":
                current_screen = GameScreen(config)

            elif screen_name == "PAUSE":
                current_screen = PauseScreen(config)

            elif screen_name == "RESUME":
                current_screen = config
                if hasattr(current_screen, "controls"):
                    current_screen.controls.paused = False

        # --- update ---
        update_result = current_screen.update()

        if isinstance(update_result, tuple):
            screen_name, config = update_result
            if screen_name == "GAME_OVER":
                current_screen = GameOverScreen(config)

        # --- draw ---
        current_screen.draw(screen)

        pygame.display.flip()
        clock.tick(ScreenConfig.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()