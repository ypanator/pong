import pygame
from pygame.locals import (
    K_w, K_s, K_UP, K_DOWN
)
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYERMOVE
)

class Player(pygame.sprite.Sprite):
    
    def __init__(self, is_left):
        super().__init__()
        self.surf = pygame.Surface((7, SCREEN_HEIGHT/4))
        self.surf.fill("white")
        self.pos = [[20, SCREEN_HEIGHT / 2], [SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2]][self.is_left]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.is_left = is_left

    def update(self, pressed_keys, dt):
        if self.is_left:
            if pressed_keys[K_w]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_s]:
                self.pos[1] += 5 * dt
        else:
            if pressed_keys[K_UP]:
                self.pos[1] -= 5 * dt
            if pressed_keys[K_DOWN]:
                self.pos[1] += 5 * dt

        if int(self.pos[1] - self.rect.centery) != 0:
            pygame.event.post(pygame.event.Event(PLAYERMOVE, is_left=self.is_left))

        self.rect.move_ip(0, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)