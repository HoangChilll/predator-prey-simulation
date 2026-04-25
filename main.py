import pygame
from ui.screens import StartScreen, MenuScreen, GameScreen, GameOverScreen

from config import ScreenConfig
from ui.effects import update_effects

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

        # --- effects ---
        update_effects()

        # --- input ---
        result = current_screen.handle_events(events)

        # 🔥 xử lý chuyển màn hình
        if result == "QUIT":
            running = False

        elif result == "START":
            current_screen = screens["START"]

        elif result == "MENU":
            current_screen = screens["MENU"]

        elif isinstance(result, tuple):
            screen_name, config = result

            if screen_name == "GAME":
                current_screen = GameScreen(config)
            elif screen_name == "GAME_OVER":
                current_screen = GameOverScreen(config)

        # Màn hình mới có thể trả về chuỗi trực tiếp
        elif result == "GAME":
            # Note: with our structure, GAME is usually a tuple ("GAME", config)
            pass

        # --- update ---
        current_screen.update()

        # --- draw ---
        current_screen.draw(screen)

        pygame.display.flip()
        clock.tick(ScreenConfig.FPS)

    pygame.quit()


if name == "main":
    main()