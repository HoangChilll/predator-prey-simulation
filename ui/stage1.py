import pygame

def draw_menu(screen, font, title_font, btn_rect):
    screen_width, screen_height = screen.get_size()

    for x in range(screen_width):
        ratio = x / screen_width
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        blue = 0
        pygame.draw.line(screen, (red, green, blue), (x, 0), (x, screen_height))
    
    # vẽ tiêu đề 
    title_text = "Predator Simulation"
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect()
    title_rect.centerx = screen_width // 2
    title_rect.centery = screen_height // 4   
    screen.blit(title_surface, title_rect)
    
    # vẽ nút bấm 
    btn_width = btn_rect.width
    btn_height = btn_rect.height
    new_btn_rect = pygame.Rect(0, 0, btn_width, btn_height)
    new_btn_rect.centerx = screen_width // 2
    new_btn_rect.centery = screen_height * 2 // 3  
    
    # vẽ nút
    COLOR_BUTTON = (0, 150, 255)
    pygame.draw.rect(screen, COLOR_BUTTON, new_btn_rect)
    
    # vẽ start
    text_surface = font.render("START", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = new_btn_rect.center
    screen.blit(text_surface, text_rect)
    return new_btn_rect