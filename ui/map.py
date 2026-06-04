import pygame

from ui.stage2 import create_ui
from ui.constants import WIDTH, HEIGHT, GRID_AREA

# SCREEN
pygame.init()
font       = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 40)
btn_rect   = pygame.Rect(220, 200, 160, 60)
buttons, dropdowns = create_ui()

_FONTS = {}


def _f(size):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("Arial", size)
    return _FONTS[size]


def get_cell(size):
    return GRID_AREA // size


def valid(pos, size):
    return True


# ── DRAW GRID ──────────────────────────────────────────────────────────────

def draw_grid(screen, grid):
    size = len(grid)
    cell = get_cell(size)

    for row in range(size):
        for col in range(size):
            rect = pygame.Rect(col * cell, row * cell, cell, cell)

            v = grid[row][col]
            if v == 1:
                color = (58, 62, 80)        # wall
            elif v == 2:
                color = (195, 105, 18)      # dynamic obstacle
            else:
                color = (20, 22, 34)        # empty cell

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (32, 36, 52), rect, 1)


# ── DRAW AGENTS ────────────────────────────────────────────────────────────

def _draw_agent(screen, cx, cy, radius, fill, glow_col, highlight):
    # Glow layers
    glow_surf = pygame.Surface((radius * 5, radius * 5), pygame.SRCALPHA)
    gc = radius * 5 // 2
    for r, a in [(radius * 2, 18), (int(radius * 1.55), 38), (int(radius * 1.2), 62)]:
        pygame.draw.circle(glow_surf, (*glow_col, a), (gc, gc), r)
    screen.blit(glow_surf, (cx - gc, cy - gc))

    # Main circle
    pygame.draw.circle(screen, fill, (cx, cy), radius)

    # Inner ring
    pygame.draw.circle(screen, highlight, (cx, cy), max(2, radius - 3), 2)

    # Specular highlight dot
    hl_r = max(2, radius // 4)
    pygame.draw.circle(screen, (255, 255, 255), (cx - radius // 3, cy - radius // 3), hl_r)


def draw_agents(screen, grey, prey, size):
    cell = get_cell(size)

    if valid(grey, size):
        cx = grey[1] * cell + cell // 2
        cy = grey[0] * cell + cell // 2
        r  = max(6, cell // 3)
        _draw_agent(screen, cx, cy, r, (210, 48, 48), (255, 50, 50), (255, 90, 90))

    if valid(prey, size):
        cx = prey[1] * cell + cell // 2
        cy = prey[0] * cell + cell // 2
        r  = max(6, cell // 3)
        _draw_agent(screen, cx, cy, r, (38, 195, 95), (40, 220, 100), (90, 245, 145))


# ── SIMULATION HUD (right panel) ───────────────────────────────────────────

def draw_sim_ui(screen, font, sim):
    px = GRID_AREA          # 600
    pw = WIDTH - px         # 200

    # Panel gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(14 + ratio * 5)
        g = int(14 + ratio * 4)
        b = int(30 + ratio * 18)
        pygame.draw.line(screen, (r, g, b), (px, y), (WIDTH - 1, y))

    # Left border accent
    pygame.draw.line(screen, (52, 82, 162), (px, 0), (px, HEIGHT), 2)

    # Header bar
    hdr = pygame.Surface((pw, 44), pygame.SRCALPHA)
    hdr.fill((18, 38, 90, 225))
    screen.blit(hdr, (px, 0))
    pygame.draw.line(screen, (62, 102, 205), (px, 44), (WIDTH, 44), 1)
    ht = _f(18).render("S I M U L A T I O N", True, (128, 172, 255))
    screen.blit(ht, ht.get_rect(center=(px + pw // 2, 22)))

    sx = px + 15  # left margin inside panel

    # ── Time
    screen.blit(_f(16).render("TIME", True, (90, 125, 182)), (sx, 56))
    screen.blit(font.render(str(sim["time"]), True, (205, 212, 255)), (sx, 76))

    # ── Turn
    screen.blit(_f(16).render("TURN", True, (90, 125, 182)), (sx, 120))
    is_pred = (sim["turn"] == "grey")
    turn_col  = (225, 72, 72)  if is_pred else (50, 208, 105)
    turn_name = "PREDATOR"     if is_pred else "PREY"
    screen.blit(_f(20).render(turn_name, True, turn_col), (sx, 140))

    # Divider
    pygame.draw.line(screen, (35, 55, 105), (px + 8, 172), (WIDTH - 8, 172), 1)

    # ── Legend
    screen.blit(_f(16).render("LEGEND", True, (90, 125, 182)), (sx, 182))

    def _legend_dot(y, fill, inner, label):
        glow_s = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, (*fill, 55), (14, 14), 13)
        screen.blit(glow_s, (sx + 1, y - 1))
        pygame.draw.circle(screen, fill, (sx + 14, y + 12), 9)
        pygame.draw.circle(screen, inner, (sx + 14, y + 12), 4)
        screen.blit(_f(18).render(label, True, (195, 198, 215)), (sx + 28, y + 4))

    _legend_dot(205, (210, 48, 48), (255, 90, 90), "Predator")
    _legend_dot(233, (38, 195, 95), (90, 245, 145), "Prey")

    # Divider 2
    pygame.draw.line(screen, (35, 55, 105), (px + 8, 262), (WIDTH - 8, 262), 1)

    # ── Status
    screen.blit(_f(16).render("STATUS", True, (90, 125, 182)), (sx, 272))
    running = sim.get("running", True)
    st_text  = "RUNNING"   if running else "STOPPED"
    st_color = (50, 208, 105) if running else (225, 72, 72)
    screen.blit(_f(19).render(st_text, True, st_color), (sx, 292))

    # Divider 3
    pygame.draw.line(screen, (35, 55, 105), (px + 8, 320), (WIDTH - 8, 320), 1)

    # Button area label
    screen.blit(_f(16).render("CONTROLS", True, (90, 125, 182)), (sx, 330))


# ── GAME OVER OVERLAY ──────────────────────────────────────────────────────

def draw_game_over(screen, font, title_font):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 165))
    screen.blit(overlay, (0, 0))

    # Glow behind text
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (200, 30, 30, 35),
                        pygame.Rect(WIDTH//2 - 180, HEIGHT//2 - 60, 360, 120))
    screen.blit(glow, (0, 0))

    # Shadow + title
    sh = title_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(sh, sh.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 27)))
    go = title_font.render("GAME OVER", True, (255, 65, 65))
    screen.blit(go, go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))

    sub = font.render("Predator caught the prey!", True, (215, 215, 215))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 22)))

    hint = _f(20).render("Press END to return", True, (110, 135, 178))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 56)))
