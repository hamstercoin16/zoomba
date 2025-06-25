import pygame
import os
import sys

# Переменные для пути к спрайтам и анимации
SPRITE_PATH = r"D:\zoomba\sprites"
SPRITE_IDLE_PREFIX = "idle-"
SPRITE_WALK_PREFIX = "walk-"
SPRITE_RUN_PREFIX = "run-"
SPRITE_JUMP_PREFIX = "jump-"

IDLE_FRAME_COUNT = 4
SPRITE_COUNT = 16
RUN_FRAME_COUNT = 8
JUMP_FRAME_COUNT = 5

TILE_SIZE = 64
GRAVITY = 1
jump_speed = 15


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
        self.last_direction = 1
        self.running = False
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

        # Загрузка кадров бега (run)
        for i in range(1, RUN_FRAME_COUNT + 1):
            path = os.path.join(SPRITE_PATH, f"{SPRITE_RUN_PREFIX}{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                pygame.quit()
                sys.exit()

        # Загрузка кадров прыжка (jump)
        for i in range(1, JUMP_FRAME_COUNT + 1):
            path = os.path.join(SPRITE_PATH, f"{SPRITE_JUMP_PREFIX}{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(img)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                pygame.quit()
                sys.exit()

        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.run()
        else:
            self.speed = 1
            self.running = False

        if keys[pygame.K_a]:
            self.direction = -1

        elif keys[pygame.K_d]:
            self.direction = 1
        else:
            self.direction = 0

    def jump(self):
        if self.on_ground:
            self.dy = -jump_speed
            self.on_ground = False

    def run(self):
        if self.on_ground:
            self.speed = 2.5
            self.running = True

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
        idle_start = 0
        walk_start = IDLE_FRAME_COUNT
        run_start = walk_start + SPRITE_COUNT
        jump_start = run_start + RUN_FRAME_COUNT

        if not self.on_ground:
            # Игрок в прыжке — используем jump-кадры
            if not jump_start <= self.frame_index < jump_start + JUMP_FRAME_COUNT:
                self.frame_index = jump_start
            self.frame_index += self.frame_speed
            if self.frame_index >= jump_start + JUMP_FRAME_COUNT:
                self.frame_index = jump_start
            self.image = self.frames[int(self.frame_index)]
            self.flipped = self.last_direction < 0

        elif self.direction != 0:
            self.last_direction = self.direction  # Запоминаем последнее направление
            if self.running:
                if not run_start <= self.frame_index < run_start + RUN_FRAME_COUNT:
                    self.frame_index = run_start
                self.frame_index += self.frame_speed
                if self.frame_index >= run_start + RUN_FRAME_COUNT:
                    self.frame_index = run_start
            else:
                if not walk_start <= self.frame_index < walk_start + SPRITE_COUNT:
                    self.frame_index = walk_start
                self.frame_index += self.frame_speed
                if self.frame_index >= walk_start + SPRITE_COUNT:
                    self.frame_index = walk_start
            self.image = self.frames[int(self.frame_index)]
            self.flipped = self.direction < 0
        else:
            self.frame_index += self.frame_speed
            if self.frame_index >= IDLE_FRAME_COUNT:
                self.frame_index = 0
            # Используем последнее направление для flip 
            self.flipped = self.last_direction < 0
            self.image = self.frames[int(self.frame_index)]

    def update(self, tiles):
        self.handle_input()
        self.move(tiles)
        self.update_animation()

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flipped, False)
        screen.blit(img, self.rect.topleft)
