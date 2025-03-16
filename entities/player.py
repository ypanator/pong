import pygame
from pygame.locals import (
    K_w, K_s, K_d, K_UP, K_DOWN, K_LEFT
)
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_FIRE_EVENT, PLAYER_OFFSET, PLAYER_WIDTH, PLAYER_HEIGHT
)

class Player(pygame.sprite.Sprite):

    def __init__(self, is_left):
        super().__init__()
        
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill("white")
        self._is_left = is_left
        self._pos = [
            PLAYER_OFFSET if self._is_left else SCREEN_WIDTH - PLAYER_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self._pos[0], self._pos[1]))
        self._score = 0


    def update(self, pressed_keys, dt):
        if self._is_left:
            if pressed_keys[K_w]:
                self._pos[1] -= 5 * dt
            if pressed_keys[K_s]:
                self._pos[1] += 5 * dt
            if pressed_keys[K_d]:
                pygame.event.post(pygame.event.Event(PLAYER_FIRE_EVENT, is_left=self._is_left))
        else:
            if pressed_keys[K_UP]:
                self._pos[1] -= 5 * dt
            if pressed_keys[K_DOWN]:
                self._pos[1] += 5 * dt
            if pressed_keys[K_LEFT]:
                pygame.event.post(pygame.event.Event(PLAYER_FIRE_EVENT, is_left=self._is_left))

        self.rect.move_ip(0, self._pos[1] - self.rect.centery)
        self._pos[1] = max(self._pos[1], PLAYER_HEIGHT / 2)
        self._pos[1] = min(self._pos[1], SCREEN_HEIGHT - PLAYER_HEIGHT / 2)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)