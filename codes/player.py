import pygame
import os
import sys

SPRITE_PATH = r"D:\zoomba\sprites"
SPRITE_WALK_PREFIX = "walk-"
SPRITE_IDLE_PREFIX = "idle-"
SPRITE_COUNT = 16  # Всего 16 кадров для анимации
IDLE_FRAME_COUNT = 4  # Кадры для стояния (например, с 1 по 4)
TILE_SIZE = 64
GRAVITY = 1
JUMP_STRENGTH = -15

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.dy = 0  # Вертикальная скорость
        self.on_ground = False
        self.frame_index = 0
        self.frame_speed = 0.2
        self.direction = 1  # -1 влево, 1 вправо, 0 стоим
        self.last_direction = 0
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.flipped = False
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def load_frames(self):
        frames = []
        
        # Загрузка кадров стояния (idle)
        for i in range(1, IDLE_FRAME_COUNT + 1):
            path = os.path.join(SPRITE_PATH, f"{SPRITE_IDLE_PREFIX}{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                pygame.quit()
                sys.exit()

        # Загрузка кадров ходьбы (walk)
        for i in range(1, SPRITE_COUNT + 1):
            path = os.path.join(SPRITE_PATH, f"{SPRITE_WALK_PREFIX}{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                pygame.quit()
                sys.exit()

        return frames

    def apply_gravity(self):
        self.dy += GRAVITY
        self.y += self.dy
        self.rect.y = self.y

    def move(self, tiles):
        self.x += self.direction * self.speed
        self.rect.x = self.x

        # Проверка горизонтальных столкновений
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.direction > 0:
                    self.rect.right = tile.left
                elif self.direction < 0:
                    self.rect.left = tile.right
                self.x = self.rect.x

        # Применить гравитацию
        self.apply_gravity()
        self.on_ground = False

        # Проверка вертикальных столкновений
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.dy > 0:
                    self.rect.bottom = tile.top
                    self.dy = 0
                    self.on_ground = True
                elif self.dy < 0:
                    self.rect.top = tile.bottom
                    self.dy = 0
                self.y = self.rect.y

    def update_animation(self):
        if self.direction != 0:
            self.last_direction = self.direction  # Запоминаем последнее направление
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.frames[IDLE_FRAME_COUNT:]):
                self.frame_index = IDLE_FRAME_COUNT
            self.flipped = self.direction < 0
        else:
            self.frame_index += self.frame_speed
            if self.frame_index >= IDLE_FRAME_COUNT:
                self.frame_index = 0
            # Используем последнее направление для flip
            self.flipped = self.last_direction < 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, tiles):
        self.move(tiles)    
        self.update_animation()

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flipped, False)
        screen.blit(img, self.rect.topleft)
