import pygame

def draw_menu(screen, font, title_font, btn_rect):
    # Lấy kích thước màn hình
    screen_width, screen_height = screen.get_size()
    
    # --- Tạo nền gradient đỏ -> xanh lục (ngang) ---
    for x in range(screen_width):
        # Tính tỉ lệ từ 0 đến 1 theo chiều ngang
        ratio = x / screen_width
        # Màu đỏ (255,0,0) đến xanh lục (0,255,0)
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        blue = 0
        pygame.draw.line(screen, (red, green, blue), (x, 0), (x, screen_height))
    
    # --- Căn giữa tiêu đề ---
    title_text = "Predator Simulation"
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect()
    title_rect.centerx = screen_width // 2
    title_rect.centery = screen_height // 4   # Đặt ở 1/4 chiều cao màn hình
    screen.blit(title_surface, title_rect)
    
    # --- Căn giữa nút bấm ---
    # Giữ nguyên kích thước của btn_rect (width, height) nhưng đặt lại vị trí giữa
    btn_width = btn_rect.width
    btn_height = btn_rect.height
    new_btn_rect = pygame.Rect(0, 0, btn_width, btn_height)
    new_btn_rect.centerx = screen_width // 2
    new_btn_rect.centery = screen_height * 2 // 3   # Đặt ở 2/3 chiều cao màn hình
    
    # Vẽ nút
    COLOR_BUTTON = (0, 150, 255)
    pygame.draw.rect(screen, COLOR_BUTTON, new_btn_rect)
    
    # --- Căn giữa chữ "START" bên trong nút ---
    text_surface = font.render("START", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = new_btn_rect.center
    screen.blit(text_surface, text_rect)
    return new_btn_rect