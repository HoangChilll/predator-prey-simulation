import pygame

pygame.font.init()
title_font = pygame.font.SysFont("arial", 48)
button_font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)

def draw_button(screen, rect, text, color, text_color=(255, 255, 255), radius=10, scale=1.0):
    """Draw button with optional scale animation"""
    if scale != 1.0:
        scaled_rect = pygame.Rect(
            rect.x - (rect.width * (scale - 1)) / 2,
            rect.y - (rect.height * (scale - 1)) / 2,
            rect.width * scale,
            rect.height * scale
        )
    else:
        scaled_rect = rect
    
    pygame.draw.rect(screen, color, scaled_rect, border_radius=radius)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=scaled_rect.center)
    screen.blit(text_surface, text_rect)

def get_button_scale(hover):
    """Tính scale animation cho button"""
    return 1.1 if hover else 1.0

def draw_exit_button(screen, exit_button, mouse_pos):
    """Vẽ nút X để tắt game"""
    hover = exit_button.collidepoint(mouse_pos)
    color = (255, 100, 100) if hover else (200, 50, 50)
    scale = 1.1 if hover else 1.0
    
    if scale != 1.0:
        scaled_rect = pygame.Rect(
            exit_button.x - (exit_button.width * (scale - 1)) / 2,
            exit_button.y - (exit_button.height * (scale - 1)) / 2,
            exit_button.width * scale,
            exit_button.height * scale
        )
    else:
        scaled_rect = exit_button
    
    pygame.draw.rect(screen, color, scaled_rect, border_radius=5)
    x_text = title_font.render("X", True, (255, 255, 255))
    x_rect = x_text.get_rect(center=scaled_rect.center)
    screen.blit(x_text, x_rect)
