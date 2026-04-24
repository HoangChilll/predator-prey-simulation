import pygame

from config import ControlConfig


def pygame_key(name):
    return getattr(pygame, f"K_{name.lower()}")


class GameControls:
    def __init__(self, config):
        self.config = config
        self.paused = False
        self.step_requested = False

        self.key_pause = pygame_key(ControlConfig.KEY_PAUSE)
        self.key_step = pygame_key(ControlConfig.KEY_STEP)
        self.key_reset = pygame_key(ControlConfig.KEY_RESET)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_pause:
                    self.paused = not self.paused

                elif event.key == self.key_step:
                    self.step_requested = True

                elif event.key == self.key_reset:
                    return ("GAME", self.config)

        return None

    def update(self, simulator):
        if not hasattr(self, 'step_timer'):
            self.step_timer = 0
            
        from config import GameConfig, ScreenConfig
        frames_per_step = ScreenConfig.FPS // GameConfig.SIMULATION_FPS
        
        should_step = False
        
        if self.step_requested:
            should_step = True
            self.step_requested = False
            self.step_timer = 0
        elif not self.paused:
            self.step_timer += 1
            if self.step_timer >= frames_per_step:
                should_step = True
                self.step_timer = 0

        if should_step:
            simulator.step()
            if not simulator.preys:
                return ("GAME_OVER", {"message": "Predator caught prey", "predator_steps": simulator.predator_steps})

        return None

    def get_status_label(self):
        return "Paused" if self.paused else "Running"

    def get_control_hint(self):
        return (
            f"{ControlConfig.KEY_PAUSE.upper()}: Pause | "
            f"{ControlConfig.KEY_STEP.upper()}: Step | "
            f"{ControlConfig.KEY_RESET.upper()}: Reset | ESC: Menu"
        )
