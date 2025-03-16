import pygame
import random
import math
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, REACHED_BORDER_EVENT, BALL_OFFSET, BALL_ACCELERATION,
    BALL_RADIUS, BALL_VELOCITY, SFX_VOLUME, BALL_PIXELS, BALL_ANGLE, PLAYER_HEIGHT, MIN_ANGLE_FACTOR
)

class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self._hit_sound = pygame.mixer.Sound("audio\\hit.wav")
        self._launch_sound = pygame.mixer.Sound("audio\\launch.wav")
        self._hit_sound.set_volume(SFX_VOLUME)
        self._launch_sound.set_volume(SFX_VOLUME)

        small_ball = pygame.Surface((BALL_PIXELS * 2, BALL_PIXELS * 2))
        small_ball.fill("black")
        pygame.draw.circle(small_ball, "white", (BALL_PIXELS, BALL_PIXELS), BALL_PIXELS)
        
        self.surf = pygame.transform.scale(small_ball, (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.surf.set_colorkey("black")

        self._is_left = random.choice([True, False])
        self._pos = [
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]
        self.rect = self.surf.get_rect(center = (self._pos[0], self._pos[1]))

        self._vel = self._xv = self._yv = 0


    def launch(self):
        factor = random.choice([-1, 1]) * random.uniform(MIN_ANGLE_FACTOR, 1)
        angle = factor * BALL_ANGLE
        self._vel = BALL_VELOCITY

        self._xv = math.cos(angle) * self._vel
        self._xv *= 1 if self._is_left else -1
        self._yv = math.sin(angle) * self._vel

        self._launch_sound.play()
        

    def handle_border(self):
        if self._pos[1] <= BALL_RADIUS:
            self._pos[1] = BALL_RADIUS + 1
            self._hit_sound.play()
            self._yv *= -1
        
        if self._pos[1] >= SCREEN_HEIGHT - BALL_RADIUS:
            self._pos[1] = SCREEN_HEIGHT - BALL_RADIUS - 1
            self._hit_sound.play()
            self._yv *= -1            

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=False))
    

    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player.rect):
                factor = (self._pos[1] - player.rect.centery) / (PLAYER_HEIGHT / 2)
                factor = math.copysign(max(MIN_ANGLE_FACTOR, abs(factor)), factor)
                angle = factor * BALL_ANGLE
                self._vel += BALL_ACCELERATION

                self._xv = math.cos(angle) * self._vel
                self._xv *= 1 if player.is_left else -1
                self._yv = math.sin(angle) * self._vel

                if player.is_left:
                    self._pos[0] = player.rect.right + BALL_RADIUS + 1
                else:
                    self._pos[0] = player.rect.left - BALL_RADIUS - 1

                self._hit_sound.play()
                break


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()
        
        self._pos[0] += self._xv * dt
        self._pos[1] += self._yv * dt

        self.rect.move_ip(self._pos[0] - self.rect.centerx, self._pos[1] - self.rect.centery)

    def follow_player(self, player_pos):
        self._pos = [
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            player_pos[1]
        ]        
        self.rect.move_ip(self._pos[0] - self.rect.centerx, self._pos[1] - self.rect.centery)
        

    def update(self, dt, is_rolling, player_pos, players):
        self.move(dt, players) if is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self._is_left = is_left
        self._pos = [
            BALL_OFFSET if self._is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self._pos[0], self._pos[1]))