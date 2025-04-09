import pygame
from pygame.locals import (
    K_w, K_s, K_d, K_UP, K_DOWN, K_LEFT
)
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PADDLE_FIRE_EVENT, PADDLE_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT
)

class OnlinePaddle(pygame.sprite.Sprite):

    def __init__(self, is_left):
        super().__init__()
        
        self.surf = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.surf.fill("white")
        self._is_left = is_left
        self._pos = [
            PADDLE_OFFSET if self._is_left else SCREEN_WIDTH - PADDLE_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self._pos[0], self._pos[1]))
        self._score = 0

    # TODO: To change
    def update(self, pressed_keys, dt):
        self.rect.move_ip(0, self._pos[1] - self.rect.centery)