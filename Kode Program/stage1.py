import pygame
import math
import random
from abc import ABC, abstractmethod

pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 180)

WIDTH = 800
HEIGHT = 600

class Object(ABC):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self.speed = 8

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x <= WIDTH - self._width:
            self.x = new_x
        if 0 <= new_y <= HEIGHT - self._height:
            self.y = new_y

    @abstractmethod
    def draw(self, screen):
        pass

class Player(Object):
    def __init__(self, x, y, width, height, spritesheet_right, spritesheet_left, spritesheet_up, spritesheet_down):
        super().__init__(x, y, width, height)
        self.frames = {
            'right': pygame.image.load(spritesheet_right).convert_alpha(),
            'left': pygame.image.load(spritesheet_left).convert_alpha(),
            'up': pygame.image.load(spritesheet_up).convert_alpha(),
            'down': pygame.image.load(spritesheet_down).convert_alpha()
        }
        self.direction = 'right'
        self.frame_index = 0
        self.frame_delay = 500
        self.health = 3
        self.blinking = False
        self.blink_duration = 1
        self.blink_timer = 0

    def move(self, dx, dy, walls, paused=False):  
        if not paused:  
            new_x = self.x + dx
            new_y = self.y + dy

            for wall in walls:
                if self.check_collision(new_x, new_y, walls):
                    return  
            super().move(dx, dy)

            if dx != 0 or dy != 0:
                if dx > 0:
                    self.direction = 'right'
                elif dx < 0:
                    self.direction = 'left'
                elif dy > 0:
                    self.direction = 'down'
                elif dy < 0:
                    self.direction = 'up'

    def check_collision(self, new_x, new_y, walls):
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        for wall in walls:
            wall_rect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)

            if player_rect.colliderect(wall_rect):
                return True  

        return False  

    def check_collision_with_enemy(self, enemy):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        if player_rect.colliderect(enemy_rect):
            self.blinking = True
            return True

        return False

    def check_collision_with_goal(self, goal):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        goal_rect = pygame.Rect(goal.x, goal.y, goal.width, goal.height)

        if player_rect.colliderect(goal_rect):
            return True

        return False

    def update_animation(self, paused=False, info=False):
        if not paused and not info:
            self.frame_index = (self.frame_index + 1) % 5 

    def draw(self, screen):
        if not self.blinking or (self.blinking and int(self.blink_timer * 5) % 2 == 0):
            frame = self.frames[self.direction].subsurface(pygame.Rect(self.frame_index * 32, 0, 32, 32))
            screen.blit(frame, (self.x, self.y))

        if self.blinking:
            self.blink_timer += 0.1

            if self.blink_timer >= self.blink_duration:
                self.blinking = False
                self.blink_timer = 0

class Enemy(Object):
    def __init__(self, start_x, start_y, end_x, end_y, width, height, sprite_image, player):
        super().__init__(start_x, start_y, width, height)
        self.sprite_image = pygame.image.load(sprite_image).convert_alpha()
        self.frame_index = 0
        self.frame_delay = 500
        self.player = player
        self.speed = 16
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.dx = end_x - start_x
        self.dy = end_y - start_y
        self.normalize_direction()
        self.moving_forward = True

    def normalize_direction(self):
        length = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if length > 0:
            self.dx /= length
            self.dy /= length

    def update(self, paused=False, info=False):
        if not paused and not info:
            if self.moving_forward:
                new_x = self.x + self.speed * self.dx
                new_y = self.y + self.speed * self.dy

                if self.at_destination():
                   self.moving_forward = False
            else:
                new_x = self.x - self.speed * self.dx
                new_y = self.y - self.speed * self.dy

                if self.at_start():
                    self.moving_forward = True

            self.x = new_x
            self.y = new_y

    def update_animation(self, paused=False, info=False):
        if not paused and not info:
            self.frame_index = (self.frame_index + 1) % 4

    def at_destination(self):
        return (self.dx > 0 and self.x >= self.end_x) or (self.dx < 0 and self.x <= self.end_x) or \
               (self.dy > 0 and self.y >= self.end_y) or (self.dy < 0 and self.y <= self.end_y)

    def at_start(self):
        return (self.dx > 0 and self.x <= self.start_x) or (self.dx < 0 and self.x >= self.start_x) or \
               (self.dy > 0 and self.y <= self.start_y) or (self.dy < 0 and self.y >= self.start_y)

    def check_collision(self, new_x, new_y, walls):
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        for wall in walls:
            wall_rect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)
            if new_rect.colliderect(wall_rect):
                return True
        return False

    def check_collision_with_player(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(enemy_rect)

    def draw(self, screen):
        frame = self.sprite_image.subsurface(pygame.Rect(self.frame_index * 32, 0, 32, 32))     
        screen.blit(frame, (self.x, self.y))

class Goal(Object):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, 32, 32)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.frame_index = 0
        self.frame_count = 0
        self.frame_delay = 3

    def draw(self, screen):
        frame = self.image.subsurface(pygame.Rect(self.frame_index * 32, 0, 32, 32))     
        screen.blit(frame, (self.x, self.y))
    
    def update_animation(self, paused=False, info=False):
        if not paused and not info:
            self.frame_count += 1
            if self.frame_count >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % 2
                self.frame_count = 0

class Wall(Object):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class PauseButton:
    def __init__(self, x, y, width, height, image_path):
        self.image_orig = pygame.image.load(image_path).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
        self.image = self.image_orig
        self.rect = self.image.get_rect(topleft=(x, y))
        self.paused = False
       
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.image = pygame.transform.scale(self.image_orig, (self.rect.width // 2, self.rect.height // 2))
        else:
            self.image = self.image_orig

class InfoButton:
    def __init__(self, x, y, width, height, image_path):
        self.image_orig = pygame.image.load(image_path).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
        self.image = self.image_orig
        self.rect = self.image.get_rect(topleft=(x, y))
        self.info = False
      
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.toggle_info()

    def toggle_info(self):
        self.info = not self.info
        if self.info:
            self.image = pygame.transform.scale(self.image_orig, (self.rect.width // 2, self.rect.height // 2))
        else:
            self.image = self.image_orig

def load_map(map_file_path):
    with open(map_file_path, 'r') as file:
        map_data = [line.strip() for line in file.readlines()]
    return map_data

def create_walls_from_map(map_data):
    walls = []
    cell_size = 32

    for row_idx, row in enumerate(map_data):
        for col_idx, cell in enumerate(row):
            if cell == 'w':
                x = col_idx * cell_size
                y = row_idx * cell_size
                wall = Wall(x, y, cell_size, cell_size, 'image/wall_stage1.png')
                walls.append(wall)

    return walls

def game_over(screen):
    font = pygame.font.Font('font/font.ttf', 50)
    text_surface = font.render("Game Over", True, "#D8D9DA")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

    return True

def game_win(screen):
    font = pygame.font.Font('font/font.ttf', 50)
    text_surface = font.render("You Win!", True, "#D8D9DA")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
    return True

def main_1():
    pygame.mixer.music.load("music/BGM.mp3")
    pygame.mixer.music.play(-3)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RUNNER MAZE")
    clock = pygame.time.Clock()

    resume_color_normal = "#D8D9DA"
    resume_color_hover = "#FFF6E0"
    back_color_normal = "#D8D9DA"
    back_color_hover = "#FFF6E0"

    goals_reached = 0
    collision_count = 0
    collision_delay = 2
    current_delay = 0

    background_image = pygame.image.load('image/background_Stage1.png').convert()

    player_spritesheet_right = 'image/player_right_stage1.png'
    player_spritesheet_left = 'image/player_left_stage1.png'
    player_spritesheet_up = 'image/player_up_stage1.png'
    player_spritesheet_down = 'image/player_down_stage1.png'
        

    player = Player(416, 288, 32, 32, player_spritesheet_right, player_spritesheet_left, player_spritesheet_up, player_spritesheet_down)

    enemies = []
    enemies.append(Enemy(304, 224, 528, 224, 32, 32, 'image/enemy_stage1.png', player))
    enemies.append(Enemy(48, 544, 720, 544, 32, 32, 'image/enemy_stage1.png', player))
    enemies.append(Enemy(48, 32, 720, 32, 32, 32, 'image/enemy_stage1.png', player))
    enemies.append(Enemy(608, 112, 608, 400, 32, 32, 'image/enemy_stage1.png', player))
    enemies.append(Enemy(96, 112, 96, 400, 32, 32, 'image/enemy_stage1.png', player))
    enemies.append(Enemy(160, 112, 160, 400, 32, 32, 'image/enemy_stage1.png', player))

    goals = []
    goals.append(Goal(96, 480, 'image/goal_stage1.png'))
    goals.append(Goal(224, 96, 'image/goal_stage1.png'))
    goals.append(Goal(384, 416, 'image/goal_stage1.png'))

    map_data = load_map('map/map1.txt')
    walls = create_walls_from_map(map_data)

    heart_full_image = pygame.image.load('image/heart_full.png').convert_alpha()
    heart_empty_image = pygame.image.load('image/heart_empty.png').convert_alpha()

    goal_full_image = pygame.image.load('image/goal_full_stage1.png').convert_alpha()
    goal_empty_image = pygame.image.load('image/goal_empty_stage1.png').convert_alpha()

    info_button = InfoButton(WIDTH - 120, 10, 40, 40, "image/info_button.png")
    pause_button = PauseButton(WIDTH - 70, 10, 40, 40, "image/pause_button.png")

    running = True
    paused = False
    info = False    
    game_over_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.rect.collidepoint(event.pos):
                    paused = not paused
                elif info_button.rect.collidepoint(event.pos):
                    info = not info                   
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over_flag:
                    return

        keys = pygame.key.get_pressed()
        if not paused and not info:
            if keys[pygame.K_2]:
                pygame.mixer.music.fadeout(1000)
            if keys[pygame.K_1]:
                pygame.mixer.music.play(-3)
            if keys[pygame.K_LEFT]:
                player.move(-player.speed, 0, walls, paused)
            if keys[pygame.K_RIGHT]:
                player.move(player.speed, 0, walls, paused)
            if keys[pygame.K_UP]:
                player.move(0, -player.speed, walls, paused)
            if keys[pygame.K_DOWN]:
                player.move(0, player.speed, walls, paused)
                
        player.update_animation(paused, info)

        for y in range(0, HEIGHT, 32):
            for x in range(0, WIDTH, 32):
                screen.blit(background_image, (x, y))
  
        player.draw(screen)

        for wall in walls:
            wall.draw(screen)

        for goal in goals:
            goal.draw(screen)
            goal.update_animation(paused, info)
            if player.check_collision_with_goal(goal):
                goals_reached += 1
                goals.remove(goal)

                if goals_reached == 3:  
                    if game_win(screen):  
                        return

        for enemy in enemies:
            enemy.update(paused, info)
            enemy.update_animation(paused, info)
            enemy.draw(screen)

            if current_delay <= 0 and player.check_collision_with_enemy(enemy):
                collision_count += 1
                player.health -= 1
                current_delay = collision_delay

                if collision_count >= 3:
                    game_over_flag = True

                if game_over_flag:
                    if game_over(screen):
                        return

        if current_delay > 0:
            current_delay -= clock.get_time() / 1000.0

        hearts_to_draw = player.health
        for i in range(3):
            heart_image = heart_full_image if hearts_to_draw > 0 else heart_empty_image
            screen.blit(heart_image, (10 + i * 40, 10))
            hearts_to_draw -= 1

        goal_to_draw = goals_reached
        for i in range(3):
            goal_image = goal_full_image if goal_to_draw > 0 else goal_empty_image
            screen.blit(goal_image, (135 + i * 35, 10))
            goal_to_draw -= 1

        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 210))
            screen.blit(overlay, (0, 0))

            font = pygame.font.Font('font/font.ttf', 36)

            resume_text_surface = font.render("RESUME", True, resume_color_normal)
            resume_text_rect = resume_text_surface.get_rect(center=(400, 300))
            screen.blit(resume_text_surface, resume_text_rect)

            back_text_surface = font.render("BACK", True, back_color_normal)
            back_text_rect = back_text_surface.get_rect(center=(400, 400))
            screen.blit(back_text_surface, back_text_rect)

            mouse_pos = pygame.mouse.get_pos()

            if resume_text_rect.collidepoint(mouse_pos):
                resume_color_normal = resume_color_hover
                if pygame.mouse.get_pressed()[0]:
                    paused = False
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            else:
                resume_color_normal = WHITE

            if back_text_rect.collidepoint(mouse_pos):
                back_color_normal = back_color_hover
                if pygame.mouse.get_pressed()[0]:
                    return
            else:
                back_color_normal = WHITE

        if info:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 210))
            screen.blit(overlay, (0, 0))

            player_info = pygame.image.load('image/player_info_stage1.png').convert_alpha()
            enemy_info = pygame.image.load('image/enemy_info_stage1.png').convert_alpha()
            heart_info = pygame.image.load('image/heart_full.png').convert_alpha()
            goal_info = pygame.image.load('image/goal_full_stage1.png').convert_alpha()
            
            player_info = pygame.transform.scale(player_info,(64, 64))
            enemy_info = pygame.transform.scale(enemy_info,(64, 64))
            heart_info = pygame.transform.scale(heart_info,(64, 64))
            goal_info = pygame.transform.scale(goal_info,(64, 64))

            screen.blit(player_info, (50, 150))
            screen.blit(enemy_info, (50, 225))
            screen.blit(heart_info, (50, 300))
            screen.blit(goal_info, (50, 375))

            font = pygame.font.Font("font/font.ttf", 50)
            stage1_text = font.render("STAGE 1", True, "#D8D9DA")
            stage1_rect = stage1_text.get_rect(center=(screen.get_width() // 2, 100))
            screen.blit(stage1_text, stage1_rect)

            info_text = [
                " = KAMU ADALAH SEEKOR ULAR YANG HARUS MELEWATI LABIRIN!",
                " = HINDARI DURI YANG ADA DI LABIRIN!",
                " = KAMU MEMILIKI TIGA NYAWA!",
                " = CARI KETIGA DAGING UNTUK MEMENANGKAN PERMAINAN",
            ]
            font = pygame.font.Font('font/font.ttf', 10)
            line_spacing = 75
            y_position = (HEIGHT - (len(info_text) * line_spacing)) // 2
            for line in info_text:
                text_surface = font.render(line, True, "#D8D9DA")
                text_rect = text_surface.get_rect(topleft=(125, y_position + 25))
                screen.blit(text_surface, text_rect)
                y_position += line_spacing

            resume_font = pygame.font.Font('font/font.ttf', 36)
            resume_text_surface = resume_font.render("RESUME", True, resume_color_normal)
            resume_text_rect = resume_text_surface.get_rect(center=(400, 500))
            screen.blit(resume_text_surface, resume_text_rect)
            
            mouse_pos = pygame.mouse.get_pos()

            if resume_text_rect.collidepoint(mouse_pos):
                resume_color_normal = resume_color_hover
                if pygame.mouse.get_pressed()[0]:
                    info = False
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            else:
                resume_color_normal = "#D8D9DA"

        
        if not info and not paused:
            pause_button.draw(screen)
            info_button.draw(screen)

        pygame.display.flip()

        clock.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main_1()