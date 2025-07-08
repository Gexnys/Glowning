import pygame
import random
import sys
import time
import json

pygame.init()

screen_width = 1920
screen_height = 1080

cloud_width = 200
cloud_height = 100

font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 60)

available_resolutions = [(1920, 1080), (1600, 900), (1366, 768), (1280, 720), (1024, 768)]
current_resolution_index = 0

def update_positions():
    global play_button_pos, exit_button_pos, settings_button_pos
    play_button_pos = (screen_width // 2 - 100, screen_height // 2 - 25)
    exit_button_pos = (screen_width // 2 - 100, screen_height // 2 + 175)
    settings_button_pos = (screen_width // 2 - 100, screen_height // 2 + 75)

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        return {'screen_width': 1920, 'screen_height': 1080}

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

settings = load_settings()

screen_width = settings['screen_width']
screen_height = settings['screen_height']

if (screen_width, screen_height) in available_resolutions:
    current_resolution_index = available_resolutions.index((screen_width, screen_height))
else:
    current_resolution_index = 0
    screen_width, screen_height = available_resolutions[0]

update_positions()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.SRCALPHA | pygame.FULLSCREEN)
pygame.display.set_caption("GW")

try:
    cloud_image = pygame.image.load('cloud.png')
    cloud_image = pygame.transform.scale(cloud_image, (cloud_width, cloud_height))
except pygame.error as e:
    print(f"Bulut görseli yüklenemedi: {e}")
    sys.exit(1)

clouds = [{"x": random.randint(0, screen_width - cloud_width), "y": random.randint(0, screen_height - cloud_height)} for _ in range(5)]

cloud_speed = 0.8

def draw_button(surface, text, pos, width=200, height=50):
    button_text = button_font.render(text, True, (255, 255, 255))
    button_rect = pygame.Rect(pos[0], pos[1], width, height)
    pygame.draw.rect(surface, (0, 0, 255), button_rect)
    surface.blit(button_text, (pos[0] + (width - button_text.get_width()) // 2, pos[1] + (height - button_text.get_height()) // 2))
    return button_rect

def draw_text(surface, text, pos, color, font_size=120, inside_box=False, box_rect=None):
    large_font = pygame.font.Font(None, font_size)
    text_surface = large_font.render(text, True, color)
    if inside_box and box_rect:
        x = box_rect.x + (box_rect.width - text_surface.get_width()) // 2
        y = box_rect.y + (box_rect.height - text_surface.get_height()) // 2
    else:
        x = pos[0] + (200 - text_surface.get_width()) // 2
        y = pos[1] - 150
    surface.blit(text_surface, (x, y))

def set_window_position():
    pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.SRCALPHA | pygame.FULLSCREEN)

def show_startup_screen():
    screen.fill((0, 0, 0))
    text = font.render("Glowning", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    try:
        anime_image = pygame.image.load('anime.png')
        anime_width = 225
        anime_height = 350
        anime_image = pygame.transform.scale(anime_image, (anime_width, anime_height))
        anime_rect = anime_image.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(anime_image, anime_rect)
    except pygame.error as e:
        print(f"Resim yüklenemedi: {e}")
    pygame.display.update()
    time.sleep(3)

running = True
show_startup_screen()
set_window_position()

color_switch_time = 2
last_color_switch = time.time()
current_color = (0, 0, 255)

def show_story_section(text, duration=6):
    box_width = 800
    box_height = 150
    box_x = (screen_width - box_width) // 2
    box_y = screen_height // 2 + 150
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, (0, 0, 0), box_rect)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, 5)
    story_font = pygame.font.Font(None, 40)
    text_surface = story_font.render(text, True, (255, 255, 255))
    max_width = box_width - 20
    text_width = text_surface.get_width()
    lines = []
    current_line = ""
    for word in text.split():
        test_line = current_line + " " + word if current_line else word
        test_surface = story_font.render(test_line, True, (255, 255, 255))
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    for i, line in enumerate(lines):
        text_surface = story_font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (box_x + 10, box_y + 10 + i * (story_font.get_height())))
    pygame.display.update()
    time.sleep(duration)
    for i in range(30):
        screen.fill((0, 0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 5)
        for i, line in enumerate(lines):
            text_surface = story_font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (box_x + 10, box_y + 10 + i * (story_font.get_height())))
        pygame.display.update()
        pygame.time.wait(100)

def typewriter_effect(text, pos, font_size=150, color=(255, 255, 255), typing_speed=0.1, inside_box=False):
    large_font = pygame.font.Font(None, font_size)
    current_text = ""
    box_width = 800
    box_height = 150
    box_x = (screen_width - box_width) // 2
    box_y = screen_height // 2 + 150
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    for i in range(len(text)):
        current_text += text[i]
        screen.fill((0, 0, 0))
        if inside_box:
            pygame.draw.rect(screen, (0, 0, 0), box_rect)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 5)
        draw_text(screen, current_text, pos, color, font_size, inside_box, box_rect)
        pygame.display.update()
        time.sleep(typing_speed)

def play_game():
    screen.fill((0, 0, 0))
    typewriter_effect("1. Bölüm", (screen_width // 2 - 100, screen_height // 2), font_size=150, color=(255, 255, 255), inside_box=False)
    time.sleep(1)
    screen.fill((0, 0, 0))
    pygame.display.update()
    time.sleep(2)
    story1 = "Test 1"
    typewriter_effect(story1, (screen_width // 2 - 60, screen_height // 2 + 150), font_size=40, inside_box=True)
    time.sleep(2)
    screen.fill((0, 0, 0))
    pygame.display.update()
    time.sleep(1)
    story2 = "Test 2"
    typewriter_effect(story2, (screen_width // 2 - 60, screen_height // 2 + 150), font_size=40, inside_box=True)
    time.sleep(2)
    screen.fill((0, 0, 0))
    pygame.display.update()
    time.sleep(1)
    story3 = "Test 3"
    typewriter_effect(story3, (screen_width // 2 - 60, screen_height // 2 + 150), font_size=40, inside_box=True)
    time.sleep(2)

def show_settings():
    global screen_width, screen_height, screen, current_resolution_index
    screen.fill((0, 0, 0))
    draw_text(screen, "Settings", (screen_width // 2 - 100, screen_height // 2 - 250), (255, 255, 255), 100)
    save_button_rect = draw_button(screen, "Save", (screen_width // 2 - 100, screen_height // 2 + 250))
    box_x = screen_width // 2 - 100
    box_y_start = screen_height // 2 - 100
    box_width = 250
    box_height = 50
    spacing = 60
    resolution_boxes = []
    for idx, (w, h) in enumerate(available_resolutions):
        box_y = box_y_start + idx * spacing
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        resolution_boxes.append((box_rect, w, h))
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)
        res_text = f"{w}x{h}"
        text_surface = button_font.render(res_text, True, (255, 255, 255))
        screen.blit(text_surface, (box_x + 10, box_y + (box_height - text_surface.get_height()) // 2))
        if (screen_width, screen_height) == (w, h):
            pygame.draw.rect(screen, (0, 255, 0), box_rect, 5)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        for idx, (box_rect, w, h) in enumerate(resolution_boxes):
            if box_rect.collidepoint(mouse_x, mouse_y):
                screen_width, screen_height = w, h
                current_resolution_index = idx
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.SRCALPHA | pygame.FULLSCREEN)
                update_positions()
                return False
        if save_button_rect.collidepoint(mouse_x, mouse_y):
            settings['screen_width'] = screen_width
            settings['screen_height'] = screen_height
            save_settings(settings)
            update_positions()
            return True
    pygame.display.update()
    return False

running = True
in_settings = False
skip_mouse = False

while running:
    screen.fill((0, 0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
    for cloud in clouds:
        cloud['x'] += cloud_speed
        if cloud['x'] > screen_width:
            cloud['x'] = -cloud_width
        screen.blit(cloud_image, (cloud['x'], cloud['y']))
    play_button_rect = draw_button(screen, "Play", play_button_pos)
    exit_button_rect = draw_button(screen, "Exit", exit_button_pos)
    settings_button_rect = draw_button(screen, "Settings", settings_button_pos)
    current_time = time.time()
    if current_time - last_color_switch > color_switch_time:
        last_color_switch = current_time
        current_color = (255, 255, 255) if current_color == (0, 0, 255) else (0, 0, 255)
    draw_text(screen, "GLOWNING", play_button_pos, current_color)
    if mouse_pressed[0] and not skip_mouse:
        if play_button_rect.collidepoint(mouse_x, mouse_y):
            play_game()
        elif exit_button_rect.collidepoint(mouse_x, mouse_y):
            running = False
        elif settings_button_rect.collidepoint(mouse_x, mouse_y):
            in_settings = True
    if in_settings:
        if show_settings():
            in_settings = False
            skip_mouse = True
    if not mouse_pressed[0]:
        skip_mouse = False
    pygame.display.update()
    pygame.time.Clock().tick(120)

pygame.quit()

#
# Bu Kod Gexnys Tarafından Yazılmıştır.
#
# İletişim için --> developergokhan@proton.me
