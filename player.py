import pygame
from pygame.locals import (
    K_w, K_s, K_d, K_UP, K_DOWN, K_LEFT
)
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_FIRE_EVENT, PLAYER_OFFSET
)

class Player(pygame.sprite.Sprite):
    OFFSET = PLAYER_OFFSET
    WIDTH, HEIGHT = 7, SCREEN_HEIGHT // 4


    def __init__(self, is_left):
        super().__init__()
        self.surf = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.surf.fill("white")
        self.is_left = is_left
        self.pos = [
            PLAYER_OFFSET if self.is_left else SCREEN_WIDTH - PLAYER_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.score = 0


    def update(self, pressed_keys, dt):
        if self.is_left:
            if pressed_keys[K_w]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_s]:
                self.pos[1] += 5 * dt
            if pressed_keys[K_d]:
                pygame.event.post(pygame.event.Event(PLAYER_FIRE_EVENT, is_left=self.is_left))
        else:
            if pressed_keys[K_UP]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_DOWN]:
                self.pos[1] += 5 * dt
            if pressed_keys[K_LEFT]:
                pygame.event.post(pygame.event.Event(PLAYER_FIRE_EVENT, is_left=self.is_left))

        self.rect.move_ip(0, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.HEIGHT / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.HEIGHT / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)