import pygame
import sys
import os
sys.path.append(os.path.dirname(__file__))  # Добавляет текущую папку в path

from player import Player


WINDOW_WIDTH, WINDOW_HEIGHT = 960, 640
TILE_SIZE = 64
FPS = 60

level_map = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "         xxx                ",
    "                            ",
    "      xxxxxxx              ",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
]

# --- Класс карты ---
class Level:
    def __init__(self, data):
        self.tiles = []
        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                if tile == 'x':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.tiles.append(rect)

    def draw(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, (100, 100, 200), tile)
              # Просто цветной квадрат

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zoomba — Тестовая карта")
clock = pygame.time.Clock()

# --- Создаём карту и игрока ---
level = Level(level_map)
player = Player(x=100, y=300)

# --- Игровой цикл ---
running = True
while running:
    screen.fill((30, 30, 40))  # Цвет фона

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление движением
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.direction = -1
    elif keys[pygame.K_RIGHT]:
        player.direction = 1
    else:
        player.direction = 0

    # Обновление
    player.update(level.tiles)

    # Отрисовка
    level.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
