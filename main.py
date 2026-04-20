import pygame
import math
import random

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project AI Hust")
clock = pygame.time.Clock()

# =========================
# FONTS
# =========================
title_font = pygame.font.SysFont("arial", 48)
button_font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)

# =========================
# GAME STATE
# =========================
game_state = "start"
running = True
screen_transition_time = 0
animation_time = 0
particles = []
is_paused = False
game_over = False
game_over_timer = 0

# =========================
# BUTTONS
# =========================
start_button = pygame.Rect(400, 350, 200, 70)
back_button = pygame.Rect(40, 40, 140, 55)
simulate_button = pygame.Rect(400, 520, 200, 70)
exit_button = pygame.Rect(920, 20, 50, 50)
reuse_button = pygame.Rect(200, 520, 240, 70)
new_button = pygame.Rect(560, 520, 240, 70)

size_buttons = [
    ("5x5", pygame.Rect(220, 230, 110, 55)),
    ("10x10", pygame.Rect(380, 230, 110, 55)),
    ("15x15", pygame.Rect(540, 230, 110, 55)),
    ("20x20", pygame.Rect(700, 230, 110, 55)),
]

algo_buttons = [
    ("BFS", pygame.Rect(220, 360, 110, 55)),
    ("DFS", pygame.Rect(380, 360, 110, 55)),
    ("A*", pygame.Rect(540, 360, 110, 55)),
]

# Simulation buttons
pause_button = pygame.Rect(750, 350, 120, 60)
stop_button = pygame.Rect(750, 440, 120, 60)

# =========================
# SETUP STATE
# =========================
selected_size = None
selected_algo = None

# Lưu ma trận cũ
last_size = None
last_algo = None
has_saved_matrix = False

# =========================
# SIMULATION STATE
# =========================
ROWS, COLS = 0, 0
CELL_SIZE = 40

predator_pos = [0, 0]
grey_pos = [0, 0]


# =========================
# HELPER FUNCTIONS
# =========================
def draw_animated_background(offset_x, offset_y):
    """Vẽ animated gradient background"""
    for y in range(0, HEIGHT, 20):
        for x in range(0, WIDTH, 20):
            wave = math.sin((x + offset_x) * 0.01 + animation_time * 0.02) * 40
            wave += math.cos((y + offset_y) * 0.01 + animation_time * 0.01) * 40
            
            color_val = int(50 + wave)
            color_val = max(20, min(120, color_val))
            
            pygame.draw.rect(screen, (color_val, color_val + 30, color_val + 60), 
                           (x, y, 20, 20))


def draw_particles():
    """Vẽ và cập nhật particles"""
    for particle in particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        particle['vy'] += 0.1
        
        if particle['life'] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])


def create_particle(x, y):
    """Tạo particle mới"""
    particles.append({
        'x': x,
        'y': y,
        'vx': random.uniform(-2, 2),
        'vy': random.uniform(-3, -1),
        'life': 100,
        'size': random.randint(2, 5),
        'color': (random.randint(100, 255), random.randint(100, 200), random.randint(150, 255))
    })


def draw_button(rect, text, color, text_color=(255, 255, 255), radius=10, scale=1.0):
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


def draw_exit_button(mouse_pos):
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


def check_predator_caught_grey():
    """Kiểm tra xem predator có bắt được grey không"""
    return predator_pos == grey_pos


def start_simulation():
    """Hàm để bắt đầu simulation"""
    global ROWS, COLS, predator_pos, grey_pos, animation_time, is_paused, game_over, game_over_timer, game_state, particles
    
    if selected_size == "5x5":
        ROWS, COLS = 5, 5
    elif selected_size == "10x10":
        ROWS, COLS = 10, 10
    elif selected_size == "15x15":
        ROWS, COLS = 15, 15
    elif selected_size == "20x20":
        ROWS, COLS = 20, 20    
    
    predator_pos = [0, 0]
    grey_pos = [ROWS - 1, COLS - 1]
    animation_time = 0
    is_paused = False
    game_over = False
    game_over_timer = 0
    particles = []

    game_state = "simulation"


def draw_start_screen(mouse_pos):
    # Animated background
    draw_animated_background(animation_time * 2, animation_time)
    
    # Particles
    draw_particles()
    if animation_time % 5 == 0:
        create_particle(mouse_pos[0], mouse_pos[1])

    # Overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill((20, 40, 80))
    screen.blit(overlay, (0, 0))

    # Title animation
    title_y = 180 + math.sin(animation_time * 0.02) * 5
    title_text = title_font.render("Project AI Hust", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title_text, title_rect)

    subtitle_text = small_font.render("Click Start to continue", True, (230, 230, 230))
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 250))
    screen.blit(subtitle_text, subtitle_rect)

    hover = start_button.collidepoint(mouse_pos)
    start_color = (255, 140, 0) if hover else (220, 120, 0)
    scale = get_button_scale(hover)

    draw_button(start_button, "Start", start_color, radius=12, scale=scale)
    draw_exit_button(mouse_pos)


def draw_setup_screen(mouse_pos):
    # Animated background
    draw_animated_background(animation_time * 2, animation_time)
    
    # Particles
    draw_particles()
    if animation_time % 5 == 0:
        create_particle(mouse_pos[0], mouse_pos[1])

    # Overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill((20, 40, 80))
    screen.blit(overlay, (0, 0))

    # Title animation
    title_y = 110 + math.sin(animation_time * 0.02) * 5
    title_text = title_font.render("Setup", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title_text, title_rect)

    size_label = button_font.render("Select Matrix Size", True, (255, 255, 255))
    screen.blit(size_label, (220, 180))

    for i, (text, rect) in enumerate(size_buttons):
        if text == selected_size:
            color = (0, 180, 0)
        elif rect.collidepoint(mouse_pos):
            color = (255, 140, 0)
        else:
            color = (220, 120, 0)

        bounce = math.sin(animation_time * 0.03 + i * 0.3) * 3
        animated_rect = pygame.Rect(rect.x, rect.y + bounce, rect.width, rect.height)
        
        scale = 1.08 if rect.collidepoint(mouse_pos) or text == selected_size else 1.0
        
        if scale != 1.0:
            scaled_rect = pygame.Rect(
                animated_rect.x - (animated_rect.width * (scale - 1)) / 2,
                animated_rect.y - (animated_rect.height * (scale - 1)) / 2,
                animated_rect.width * scale,
                animated_rect.height * scale
            )
        else:
            scaled_rect = animated_rect
        
        pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
        text_surface = button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

    algo_label = button_font.render("Select Algorithm", True, (255, 255, 255))
    screen.blit(algo_label, (220, 310))

    for i, (text, rect) in enumerate(algo_buttons):
        if text == selected_algo:
            color = (0, 180, 0)
        elif rect.collidepoint(mouse_pos):
            color = (255, 140, 0)
        else:
            color = (220, 120, 0)

        bounce = math.sin(animation_time * 0.03 + i * 0.3) * 3
        animated_rect = pygame.Rect(rect.x, rect.y + bounce, rect.width, rect.height)
        
        scale = 1.08 if rect.collidepoint(mouse_pos) or text == selected_algo else 1.0
        
        if scale != 1.0:
            scaled_rect = pygame.Rect(
                animated_rect.x - (animated_rect.width * (scale - 1)) / 2,
                animated_rect.y - (animated_rect.height * (scale - 1)) / 2,
                animated_rect.width * scale,
                animated_rect.height * scale
            )
        else:
            scaled_rect = animated_rect
        
        pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
        text_surface = button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

    info_size = small_font.render(f"Selected size: {selected_size}", True, (255, 255, 255))
    info_algo = small_font.render(f"Selected algorithm: {selected_algo}", True, (255, 255, 255))
    screen.blit(info_size, (220, 470))
    screen.blit(info_algo, (220, 500))

    # Hiển thị Simulate nếu KHÔNG có ma trận cũ
    if not has_saved_matrix:
        if selected_size and selected_algo:
            if simulate_button.collidepoint(mouse_pos):
                sim_color = (0, 220, 0)
            else:
                sim_color = (0, 180, 0)
            scale = 1.1 if simulate_button.collidepoint(mouse_pos) else 1.0
        else:
            sim_color = (120, 120, 120)
            scale = 1.0

        draw_button(simulate_button, "Simulate", sim_color, radius=12, scale=scale)
    
    # Hiển thị Reuse và New nếu CÓ ma trận cũ
    if has_saved_matrix:
        reuse_hover = reuse_button.collidepoint(mouse_pos)
        reuse_color = (100, 200, 100) if reuse_hover else (50, 150, 50)
        scale = 1.08 if reuse_hover else 1.0
        draw_button(reuse_button, f"Reuse: {last_size}/{last_algo}", reuse_color, radius=12, scale=scale)
        
        # Nút New
        new_hover = new_button.collidepoint(mouse_pos)
        new_color = (100, 180, 255) if new_hover else (50, 120, 200)
        scale = 1.08 if new_hover else 1.0
        draw_button(new_button, "New Setup", new_color, radius=12, scale=scale)

    hover = back_button.collidepoint(mouse_pos)
    back_color = (255, 140, 0) if hover else (220, 120, 0)
    draw_button(back_button, "Back", back_color, scale=get_button_scale(hover))

    draw_exit_button(mouse_pos)


def draw_simulation_screen(mouse_pos):
    # Animated background
    draw_animated_background(animation_time * 2, animation_time)
    
    # Particles
    draw_particles()

    # Overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)
    overlay.fill((30, 30, 30))
    screen.blit(overlay, (0, 0))

    grid_x = 80
    grid_y = 120
    grid_width = 600
    grid_height = 600

    panel_x = grid_x + grid_width + 40

    cell_width = grid_width // COLS
    cell_height = grid_height // ROWS
    cell_size = min(cell_width, cell_height)

    # Draw grid với animation
    for row in range(ROWS):
        for col in range(COLS):
            offset = math.sin(animation_time * 0.01 + (row + col) * 0.1) * 0.5
            
            rect = pygame.Rect(
                grid_x + col * cell_size,
                grid_y + row * cell_size,
                cell_size,
                cell_size
            )
            grid_color = (200 + int(offset * 10), 200 + int(offset * 10), 200 + int(offset * 10))
            pygame.draw.rect(screen, grid_color, rect, 1)

    # Predator animation
    predator_bob = math.sin(animation_time * 0.05) * 3
    predator_rect = pygame.Rect(
        grid_x + predator_pos[1] * cell_size,
        grid_y + predator_pos[0] * cell_size + predator_bob,
        cell_size,
        cell_size
    )
    pygame.draw.rect(screen, (255, 0, 0), predator_rect)
    pygame.draw.rect(screen, (255, 100, 100), predator_rect, 3)

    # Grey animation
    grey_bob = math.sin(animation_time * 0.04 + 1) * 3
    grey_rect = pygame.Rect(
        grid_x + grey_pos[1] * cell_size,
        grid_y + grey_pos[0] * cell_size + grey_bob,
        cell_size,
        cell_size
    )
    pygame.draw.rect(screen, (130, 130, 130), grey_rect)
    pygame.draw.rect(screen, (180, 180, 180), grey_rect, 3)

    # Title/info
    sim_title = title_font.render("Simulation", True, (255, 255, 255))
    screen.blit(sim_title, (panel_x, 120))

    info1 = button_font.render(f"Size: {selected_size}", True, (255, 255, 255))
    info2 = button_font.render(f"Algorithm: {selected_algo}", True, (255, 255, 255))
    screen.blit(info1, (panel_x, 230))
    screen.blit(info2, (panel_x, 280))

    # Pause button
    pause_hover = pause_button.collidepoint(mouse_pos)
    pause_color = (255, 200, 0) if pause_hover else (200, 150, 0)
    pause_text = "Resume" if is_paused else "Pause"
    scale = 1.08 if pause_hover else 1.0
    
    if scale != 1.0:
        scaled_pause = pygame.Rect(
            pause_button.x - (pause_button.width * (scale - 1)) / 2,
            pause_button.y - (pause_button.height * (scale - 1)) / 2,
            pause_button.width * scale,
            pause_button.height * scale
        )
    else:
        scaled_pause = pause_button
    
    pygame.draw.rect(screen, pause_color, scaled_pause, border_radius=8)
    pause_surf = small_font.render(pause_text, True, (255, 255, 255))
    pause_rect = pause_surf.get_rect(center=scaled_pause.center)
    screen.blit(pause_surf, pause_rect)

    # Stop button
    stop_hover = stop_button.collidepoint(mouse_pos)
    stop_color = (255, 100, 100) if stop_hover else (200, 50, 50)
    scale = 1.08 if stop_hover else 1.0
    
    if scale != 1.0:
        scaled_stop = pygame.Rect(
            stop_button.x - (stop_button.width * (scale - 1)) / 2,
            stop_button.y - (stop_button.height * (scale - 1)) / 2,
            stop_button.width * scale,
            stop_button.height * scale
        )
    else:
        scaled_stop = stop_button
    
    pygame.draw.rect(screen, stop_color, scaled_stop, border_radius=8)
    stop_surf = small_font.render("Stop", True, (255, 255, 255))
    stop_rect = stop_surf.get_rect(center=scaled_stop.center)
    screen.blit(stop_surf, stop_rect)

    # Back button
    hover = back_button.collidepoint(mouse_pos)
    back_color = (255, 140, 0) if hover else (220, 120, 0)
    draw_button(back_button, "Back", back_color, scale=get_button_scale(hover))

    # Pause text
    if is_paused:
        pause_text_display = title_font.render("PAUSED", True, (255, 200, 0))
        pause_text_rect = pause_text_display.get_rect(center=(grid_x + grid_width // 2, grid_y + grid_height // 2))
        screen.blit(pause_text_display, pause_text_rect)

    # Game Over text
    if game_over:
        caught_text = title_font.render("GREY CAUGHT!", True, (255, 0, 0))
        caught_rect = caught_text.get_rect(center=(grid_x + grid_width // 2, grid_y + grid_height // 2))
        screen.blit(caught_text, caught_rect)

    draw_exit_button(mouse_pos)

# =========================
# MAIN LOOP
# =========================
while running:
    mouse_pos = pygame.mouse.get_pos()
    animation_time += 1
    screen_transition_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.collidepoint(event.pos):
                running = False

        if game_state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = "setup"
                    screen_transition_time = 0
                    particles = []

        elif game_state == "setup":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    game_state = "start"
                    screen_transition_time = 0
                    particles = []
                    selected_size = None
                    selected_algo = None

                for text, rect in size_buttons:
                    if rect.collidepoint(event.pos):
                        selected_size = text

                for text, rect in algo_buttons:
                    if rect.collidepoint(event.pos):
                        selected_algo = text

                # Nút Simulate - chỉ hiển thị nếu không có reuse
                if not has_saved_matrix and simulate_button.collidepoint(event.pos):
                    if selected_size and selected_algo:
                        last_size = selected_size
                        last_algo = selected_algo
                        has_saved_matrix = True
                        start_simulation()

                # Nút Reuse - trực tiếp vào simulation
                if has_saved_matrix and reuse_button.collidepoint(event.pos):
                    start_simulation()

                # Nút New - reset để chọn lại
                if has_saved_matrix and new_button.collidepoint(event.pos):
                    has_saved_matrix = False
                    selected_size = None
                    selected_algo = None
                    last_size = None
                    last_algo = None

        elif game_state == "simulation":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    game_state = "setup"
                    screen_transition_time = 0
                    is_paused = False
                    game_over = False
                    particles = []

                if pause_button.collidepoint(event.pos):
                    is_paused = not is_paused

                if stop_button.collidepoint(event.pos):
                    game_state = "setup"
                    screen_transition_time = 0
                    is_paused = False
                    game_over = False
                    particles = []

    # Kiểm tra predator bắt được grey
    if game_state == "simulation" and not game_over:
        if check_predator_caught_grey():
            game_over = True
            game_over_timer = 0

    # Tự động quay về setup sau 3 giây khi game over
    if game_over:
        game_over_timer += 1
        if game_over_timer > 180:  # 3 giây ở 60 FPS
            game_state = "setup"
            is_paused = False
            game_over = False
            particles = []

    if game_state == "start":
        draw_start_screen(mouse_pos)

    elif game_state == "setup":
        draw_setup_screen(mouse_pos)

    elif game_state == "simulation":
        draw_simulation_screen(mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()