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

        self.hit_sound = pygame.mixer.Sound("audio\\hit.wav")
        self.launch_sound = pygame.mixer.Sound("audio\\launch.wav")
        self.hit_sound.set_volume(SFX_VOLUME)
        self.launch_sound.set_volume(SFX_VOLUME)

        small_ball = pygame.Surface((BALL_PIXELS * 2, BALL_PIXELS * 2))
        small_ball.fill("black")
        pygame.draw.circle(small_ball, "white", (BALL_PIXELS, BALL_PIXELS), BALL_PIXELS)
        
        self.surf = pygame.transform.scale(small_ball, (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.surf.set_colorkey("black")

        self.is_left = random.choice([True, False])
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))

        self.vel = self.xv = self.yv = 0


    def launch(self):
        factor = random.choice([-1, 1]) * random.uniform(MIN_ANGLE_FACTOR, 1)
        angle = factor * BALL_ANGLE
        self.vel = BALL_VELOCITY

        self.xv = math.cos(angle) * self.vel
        self.xv *= 1 if self.is_left else -1
        self.yv = math.sin(angle) * self.vel

        self.launch_sound.play()
        

    def handle_border(self):
        if self.pos[1] <= BALL_RADIUS:
            self.pos[1] = BALL_RADIUS + 1
            self.hit_sound.play()
            self.yv *= -1
        
        if self.pos[1] >= SCREEN_HEIGHT - BALL_RADIUS:
            self.pos[1] = SCREEN_HEIGHT - BALL_RADIUS - 1
            self.hit_sound.play()
            self.yv *= -1            

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=False))
    

    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player.rect):
                factor = (self.pos[1] - player.rect.centery) / (PLAYER_HEIGHT / 2)
                factor = math.copysign(max(MIN_ANGLE_FACTOR, abs(factor)), factor)
                angle = factor * BALL_ANGLE
                self.vel += BALL_ACCELERATION

                self.xv = math.cos(angle) * self.vel
                self.xv *= 1 if player.is_left else -1
                self.yv = math.sin(angle) * self.vel

                if player.is_left:
                    self.pos[0] = player.rect.right + BALL_RADIUS + 1
                else:
                    self.pos[0] = player.rect.left - BALL_RADIUS - 1

                self.hit_sound.play()
                break


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()
        
        self.pos[0] += self.xv * dt
        self.pos[1] += self.yv * dt

        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)

    def follow_player(self, player_pos):
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            player_pos[1]
        ]        
        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        

    def update(self, dt, is_rolling, player_pos, players):
        self.move(dt, players) if is_rolling else self.follow_player(player_pos)


    def reset(self, is_left):
        self.is_left = is_left
        self.pos = [
            BALL_OFFSET if self.is_left else SCREEN_WIDTH - BALL_OFFSET,
            SCREEN_HEIGHT // 2
        ]        
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))