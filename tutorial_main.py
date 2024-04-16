import pygame
from pygame.locals import *
import random

def add_border(parent_surface, parent_rect, border_size):
        new_surf = pygame.Surface((parent_surface.get_width() + border_size, parent_surface.get_height() + border_size))
        new_surf.fill("red")
        new_surf.blit(parent_surface, parent_rect)
        return new_surf

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.pos = [0, 0]
        self.surf = add_border(self.surf, self.rect, 2)

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.pos[1] -= 5 * dt
            move_up_sound.play()
        if pressed_keys[K_s]:
            self.pos[1] += 5 * dt
            move_down_sound.play()            
        if pressed_keys[K_a]:
            self.pos[0] -= 5 * dt
        if pressed_keys[K_d]:
            self.pos[0] += 5 * dt
        
        self.rect.move_ip(self.pos[0] - self.rect.left, self.pos[1] - self.rect.top)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.pos = [
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
        ]
        self.rect = self.surf.get_rect(
            left = self.pos[0],
            top = self.pos[1]
        )
        self.speed = random.randint(7, 20) + extra_speed
        self.surf = add_border(self.surf, self.rect, 2)
    
    def update(self):
        self.pos[0] -= self.speed * dt
        self.rect.move_ip(self.pos[0] - self.rect.left, self.pos[1] - self.rect.top)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.pos = [
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT)
        ]
        self.rect = self.surf.get_rect(
            left = self.pos[0],
            top = self.pos[1]
        )
    
    def update(self):
        self.pos[0] -= 5 * dt
        self.rect.move_ip(self.pos[0] - self.rect.left, self.pos[1] - self.rect.top)
        if self.rect.right < 0:
            self.kill()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

extra_speed = 0
missiles_count = 0
clock = pygame.time.Clock()
dt = clock.tick() / 1000.0 * 60
ADDENEMY = USEREVENT + 1
ADDCLOUD = USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDCLOUD, 300)

entities = pygame.sprite.Group()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
clouds_behind = pygame.sprite.Group()
clouds_front = pygame.sprite.Group()

player = Player()
entities.add(player)

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops = -1)

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in (K_ESCAPE, K_q):
                running = False
        
        elif event.type == QUIT:
            running = False

        if event.type == ADDENEMY:
            new_enemy = Enemy()
            entities.add(new_enemy)
            enemies.add(new_enemy)
            missiles_count += 1
            if missiles_count % 10 == 0:
                extra_speed += 1

        if event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            position = random.choice(("front", "behind"))
            if position == "front":
                clouds_front.add(new_cloud)
            else:
                clouds_behind.add(new_cloud)


    player.update(pygame.key.get_pressed())
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_down_sound.stop()
        move_up_sound.stop()
        collision_sound.play()
        running = False
    
    dt = clock.tick() / 1000.0 * 60

    clouds.update()
    enemies.update()
    screen.fill((135, 206, 250))
    for cloud in clouds_behind:
        screen.blit(cloud.surf, cloud.rect)
    for entity in entities:
        screen.blit(entity.surf, entity.rect)
    for cloud in clouds_front:
        screen.blit(cloud.surf, cloud.rect)
    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()        