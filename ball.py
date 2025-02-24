import pygame
import random
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, REACHED_BORDER_EVENT, BALL_OFFSET, 
    BALL_RADIUS, BALL_VEL, SFX_VOLUME, BALL_PIXELS
)

class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.hit_sound = pygame.mixer.Sound("audio\hit.wav")
        self.launch_sound = pygame.mixer.Sound("audio\launch.wav")
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
        self.hit_bottom, self.hit_top = False, False
        self.cur_vel = [0, 0]


    def launch(self):
        self.launch_sound.play()
        if self.is_left:
            self.cur_vel = BALL_VEL
        else:
            self.cur_vel = [-BALL_VEL[0], BALL_VEL[1]]
        

    def handle_border(self):
        if self.rect.top <= 0 and not self.hit_top:
            self.hit_top, self.hit_bottom = True, False
            # print("playing sound")
            self.hit_sound.play()
            self.cur_vel[1] *= -1
        
        if self.rect.bottom >= SCREEN_HEIGHT and not self.hit_bottom:
            self.hit_top, self.hit_bottom = False, True
            # print("playing sound")
            self.hit_sound.play()
            self.cur_vel[1] *= -1            

        if self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=True))
        elif self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(REACHED_BORDER_EVENT, is_left=False))
    

    def handle_player(self, players):
        for player in players:
            if self.rect.colliderect(player.rect):
                self.cur_vel = [self.cur_vel[0] * -1, self.cur_vel[1]]
                if player.is_left:
                    self.pos[0] = player.rect.right + BALL_RADIUS
                else:
                    self.pos[0] = player.rect.left - BALL_RADIUS
                self.hit_sound.play()


    def move(self, dt, players):
        self.handle_player(players)
        self.handle_border()

        self.pos[0] += self.cur_vel[0] * dt
        self.pos[1] += self.cur_vel[1] * dt

        self.rect.move_ip(self.pos[0] - self.rect.centerx, self.pos[1] - self.rect.centery)
        self.pos[1] = max(self.pos[1], self.surf.get_height() / 2)
        self.pos[1] = min(self.pos[1], SCREEN_HEIGHT - self.surf.get_height() / 2)


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
        self.cur_vel = [0, 0]