import pygame
import random

from maze_generator import generate_maze


pygame.init()

# Створення вікна гри
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Втеча з лабіринту')

# Фоновий колір
background_color = (0, 0, 0)  # Чорний колір фону
cell_size = 20

pygame.mixer.music.load("assets/background.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

sound_key = pygame.mixer.Sound("assets/sound_key.mp3")
sound_key.set_volume(1.0)

sound_door = pygame.mixer.Sound("assets/sound_door.mp3")
sound_door.set_volume(1.0)

wall_img = pygame.image.load("assets/wall.png")
wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))

key_img = pygame.image.load("assets/key.png")
key_img = pygame.transform.scale(key_img, (cell_size, cell_size))

door_img = pygame.image.load("assets/door.png")
door_img = pygame.transform.scale(door_img, (cell_size, cell_size))

player_img = [pygame.image.load(f"assets/player{i}.png") for i in range(1, 5)]
player_img = [pygame.transform.scale(player, (cell_size, cell_size)) for player in player_img]
player_id = 0

background_img = pygame.image.load("assets/background.png")
background_img = pygame.transform.scale(background_img, (800, 600))


def draw_button(screen, text, color, x, y, w, h):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (w - text_surface.get_width()) / 2, y + (h - text_surface.get_height()) / 2))


def main_menu():
    menu_is_running = True
    while menu_is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_is_running = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 200 <= y <= 300:
                    menu_is_running = False
                elif 150 <= x <= 650 and 350 <= y <= 450:
                    menu_is_running = False
                    exit()

        screen.blit(background_img, (0, 0))
        draw_button(screen, "почати гру", (0, 150, 0), 150, 200, 500, 100)
        draw_button(screen, "вийти", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()

def win():
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 200 <= y <= 300:
                    win = False
                elif 150 <= x <= 650 and 350 <= y <= 450:
                    win = False
                    exit()
        
        screen.blit(background_img, (0, 0))
        draw_button(screen, "Вітаю! Ти пройшов гру!", (0,150,0), 150, 200, 500, 100)
        draw_button(screen, "Вийти", (200,0,0), 150, 350, 500, 100)
        pygame.display.flip()

main_menu()

maze = generate_maze(30, 40)

height = len(maze)
width = len(maze[0])

free_cells = []
for y in range(height):
    for x in range(width):
        if maze [y][x] == 0:
            free_cells.append((x, y))

door_position = free_cells[-1]
key_position = random.choice(free_cells[1:-1])
player_x, player_y = free_cells[0]
has_key = False

clock = pygame.time.Clock()

fps = 15

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] == 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < width - 1 and maze[player_y][player_x + 1] == 0:
                player_x += 1
            elif event.key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] == 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < height - 1 and maze[player_y + 1][player_x] == 0:
                player_y += 1

    # Заповнюємо екран фоном
    screen.fill(background_color)

    for y in range(height):
        for x in range(width):
            if maze [y][x] == 1:
                screen.blit(wall_img, (x * cell_size, y * cell_size))

    if not has_key:
        if (player_x, player_y) == key_position:
            has_key = True
            sound_key.play()
        else:
            screen.blit(key_img, (key_position[0] * cell_size, key_position[1] * cell_size))

    screen.blit(door_img, (door_position[0] * cell_size, door_position[1] * cell_size))
    screen.blit(player_img[player_id], (player_x * cell_size, player_y * cell_size))
    player_id = (player_id + 1) % len(player_img)

    if has_key and (player_x, player_y) == door_position:
        running = False
        sound_door.play()
    # Оновлюємо екран
    pygame.display.flip()

    clock.tick(fps)

win()
pygame.quit()