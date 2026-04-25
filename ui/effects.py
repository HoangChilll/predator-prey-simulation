import math
import random
import pygame

class EffectsState:
    animation_time = 0
    particles = []

def draw_animated_background(screen, width, height, offset_x, offset_y):
    """Vẽ animated gradient background"""
    for y in range(0, height, 20):
        for x in range(0, width, 20):
            wave = math.sin((x + offset_x) * 0.01 + EffectsState.animation_time * 0.02) * 40
            wave += math.cos((y + offset_y) * 0.01 + EffectsState.animation_time * 0.01) * 40
            
            color_val = int(50 + wave)
            color_val = max(20, min(120, color_val))
            
            pygame.draw.rect(screen, (color_val, color_val + 30, color_val + 60), 
                           (x, y, 20, 20))

def draw_particles(screen):
    """Vẽ và cập nhật particles"""
    for particle in EffectsState.particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['life'] -= 1
        particle['vy'] += 0.1
        
        if particle['life'] <= 0:
            EffectsState.particles.remove(particle)
        else:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])

def create_particle(x, y):
    """Tạo particle mới"""
    EffectsState.particles.append({
        'x': x,
        'y': y,
        'vx': random.uniform(-2, 2),
        'vy': random.uniform(-3, -1),
        'life': 100,
        'size': random.randint(2, 5),
        'color': (random.randint(100, 255), random.randint(100, 200), random.randint(150, 255))
    })

def update_effects():
    EffectsState.animation_time += 1
