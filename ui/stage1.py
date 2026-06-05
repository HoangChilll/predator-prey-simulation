import pygame
import math

_FONTS = {}


def _f(size):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("Arial", size)
    return _FONTS[size]


def draw_menu(screen, font, title_font, btn_rect):
    w, h = screen.get_size()
    t = pygame.time.get_ticks() / 1000.0

    # vẽ background
    for y in range(h):
        ratio = y / h
        r = int(10 + ratio * 8)
        g = int(10 + ratio * 6)
        b = int(32 + ratio * 22)
        pygame.draw.line(screen, (r, g, b), (0, y), (w, y))
    grid_s = pygame.Surface((w, h), pygame.SRCALPHA)
    for x in range(0, w + 1, 55):
        pygame.draw.line(grid_s, (70, 95, 160, 13), (x, 0), (x, h))
    for y in range(0, h + 1, 55):
        pygame.draw.line(grid_s, (70, 95, 160, 13), (0, y), (w, y))
    screen.blit(grid_s, (0, 0))
    pulse = 0.5 + 0.5 * math.sin(t * 1.8)
    glow_s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.circle(glow_s, (25, 55, 135, int(28 + 22 * pulse)),
                       (w // 2, h // 4), int(115 + 30 * pulse))
    screen.blit(glow_s, (0, 0))
    title_cy = h // 4
    for dx, dy in [(4, 4), (2, 2)]:
        sh = title_font.render("PREDATOR  &  PREY", True, (5, 5, 15))
        screen.blit(sh, sh.get_rect(center=(w // 2 + dx, title_cy + dy)))
    title_s = title_font.render("PREDATOR  &  PREY", True, (255, 210, 55))
    screen.blit(title_s, title_s.get_rect(center=(w // 2, title_cy)))
    sub = _f(20).render("Intelligent Agent Simulation", True, (135, 162, 212))
    screen.blit(sub, sub.get_rect(center=(w // 2, title_cy + 46)))
    lw, ly, mx = 210, title_cy + 70, w // 2
    pygame.draw.line(screen, (75, 115, 200), (mx - lw // 2, ly), (mx - 12, ly - 8), 2)
    pygame.draw.line(screen, (255, 210, 55), (mx - 12, ly - 8), (mx + 12, ly - 8), 2)
    pygame.draw.line(screen, (75, 115, 200), (mx + 12, ly - 8), (mx + lw // 2, ly), 2)

    # vẽ agnents
    rl_y = int(h * 0.52)
    # kẻ săn mồi prey màu đỏ
    px_p = w // 2 - 110
    glow_p = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(glow_p, (210, 50, 50, 60), (18, 18), 16)
    screen.blit(glow_p, (px_p - 18, rl_y - 18))
    pygame.draw.circle(screen, (210, 55, 55), (px_p, rl_y), 9)
    pygame.draw.circle(screen, (255, 100, 100), (px_p, rl_y), 4)
    ps = _f(20).render("PREDATOR", True, (205, 135, 135))
    screen.blit(ps, (px_p + 14, rl_y - ps.get_height() // 2))

    # con mồi grey màu xanh
    px_q = w // 2 + 60
    glow_q = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(glow_q, (40, 200, 100, 60), (18, 18), 16)
    screen.blit(glow_q, (px_q - 18, rl_y - 18))
    pygame.draw.circle(screen, (40, 200, 100), (px_q, rl_y), 9)
    pygame.draw.circle(screen, (90, 240, 145), (px_q, rl_y), 4)
    qs = _f(20).render("PREY", True, (135, 200, 155))
    screen.blit(qs, (px_q + 14, rl_y - qs.get_height() // 2))

    #  nút bấm START 
    bw, bh = 182, 52
    new_btn = pygame.Rect(0, 0, bw, bh)
    new_btn.centerx = w // 2
    new_btn.centery = int(h * 0.68)
    hover = new_btn.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, (0, 0, 0), new_btn.move(4, 4), border_radius=14)
    pygame.draw.rect(screen, (50, 130, 240) if hover else (28, 98, 210),
                     new_btn, border_radius=14)
    sheen = pygame.Surface((bw - 10, bh // 2 - 4), pygame.SRCALPHA)
    sheen.fill((255, 255, 255, 22))
    screen.blit(sheen, (new_btn.x + 5, new_btn.y + 4))
    pygame.draw.rect(screen, (130, 188, 255) if hover else (75, 138, 218),
                     new_btn, width=2, border_radius=14)
    # chữ
    btxt = font.render("> START", True, (255, 255, 255))
    screen.blit(btxt, btxt.get_rect(center=new_btn.center))
    hint = _f(18).render("Click to configure simulation", True, (85, 110, 158))
    screen.blit(hint, hint.get_rect(center=(w // 2, new_btn.bottom + 18)))
    return new_btn
