import pygame
from pygame.locals import (
    K_q, K_w, K_s, K_SPACE, K_ESCAPE, KEYDOWN, QUIT
)

from scenes.game.online_entities.online_paddle import OnlinePaddle
from .local_entities.score import Score
from .local_entities.ball import Ball
from .local_entities.middle_line import MiddleLine

from constants import (
    PADDLE_FIRE_EVENT, REACHED_BORDER_EVENT, SFX_VOLUME
)

import logging
from net.server.online_game.models import Inputs
import net.server.server_codes as codes
from .online_entities.room_code import RoomCode

class OnlineGameScene:
    def __init__(self, scene_manager):
        self._scene_manager = scene_manager

        self._logger = logging.getLogger(__name__)
        self._client = self._scene_manager.context["client"]
        assert self._client is not None

        self._send_inputs_timestamp = pygame.time.get_ticks()
        self._send_inputs_timestep = 16
        self._inputs = Inputs()

        self._screen = pygame.display.get_surface()

        self._reachedborder_sound = pygame.mixer.Sound("audio\\reachedborder.wav")
        self._reachedborder_sound.set_volume(SFX_VOLUME)

        self._ball = Ball()
        self._paddle_left = OnlinePaddle(True)
        self._paddle_right = OnlinePaddle(False)
        self._score_left = Score(True)
        self._score_right = Score(False)
        self._middle_line = MiddleLine()
        self._room_code = RoomCode()

        self._drawables = pygame.sprite.Group()
        self._paddles = pygame.sprite.Group()
        self._drawables.add(self._paddle_left, self._paddle_right, self._ball, self._score_left, self._score_right, self._middle_line, self._room_code)
        self._paddles.add(self._paddle_left, self._paddle_right)

        self._is_rolling = False


    def iterate(self, tick):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    self._scene_manager.change_scene("OnlineMenuScene")
            
            if event.type == QUIT:
                self._scene_manager.close()
            
            if (
                not self._is_rolling and event.type == PADDLE_FIRE_EVENT and 
                event.is_left == self._ball._is_left
            ):
                self._ball.launch()
                self._is_rolling = True

            if event.type == REACHED_BORDER_EVENT:
                self._reachedborder_sound.play()
                if event.is_left: 
                    self._paddle_right._score += 1
                    self._score_right.update(self._paddle_right._score)
                else: 
                    self._paddle_left._score += 1
                    self._score_left.update(self._paddle_left._score)

                self._ball.reset(event.is_left)
                self._is_rolling = False

        dt = tick / 1000 * 60
        pressed_keys = pygame.key.get_pressed()
        self._paddles.update(pygame.key.get_pressed(), dt)
        self._ball.update(dt, self._is_rolling, 
            self._paddle_left._pos if self._ball._is_left else self._paddle_right._pos, self._paddles
        )
        self._handle_messages()

        if pygame.time.get_ticks() - self._send_inputs_timestamp > self._send_inputs_timestep:
            self._inputs["up"] = pressed_keys[K_w]
            self._inputs["down"] = pressed_keys[K_s]
            self._inputs["fire"] = pressed_keys[K_SPACE]
            self._client.send_new_inputs(self._inputs)
            self._send_inputs_timestamp = pygame.time.get_ticks()
            
        self._screen.fill("black")
        for ent in self._drawables:
            self._screen.blit(ent.surf, ent.rect)
            
        pygame.display.flip()
    
    def _handle_messages(self):  # Debug print
        while (msg := self._client.read()) is not None:
            print(f"Received message: {msg}")  # More detailed print
            type = msg["type"]
            if type == codes.ROOM_CODE:
                self._room_code.update(msg["data"])
                print("Updated room code")
            elif type == codes.NEW_STATE:
                print("Got new state")  # Debug print
                self._inject_state(msg["data"])

            elif type == codes.ERROR:
                self._logger.error(msg)
            
            else:
                self._logger.debug(msg)
        
    def _inject_state(self, state):
        lpaddle_state = state["paddles"][0]
        rpaddle_state = state["paddles"][1]
        ball_state = state["ball"]

        self._paddle_left._pos[0] = lpaddle_state["x"]
        self._paddle_left._pos[1] = lpaddle_state["y"]
        self._paddle_left._score = lpaddle_state["score"]

        self._paddle_right._pos[0] = rpaddle_state["x"]
        self._paddle_right._pos[1] = rpaddle_state["y"]
        self._paddle_right._score = rpaddle_state["score"]

        self._ball._is_left = ball_state["is_left"]
        self._ball.is_rolling = ball_state["is_rolling"]
        self._ball._pos[0] = ball_state["x"]
        self._ball._pos[1] = ball_state["y"]
        self._ball._xv = ball_state["xv"]
        self._ball._yv = ball_state["yv"]
        self._ball._vel = ball_state["vel"]

        self._score_left.update(self._paddle_left._score)
        self._score_right.update(self._paddle_right._score)