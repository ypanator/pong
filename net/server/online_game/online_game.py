from .entities.ball import Ball
from .entities.paddle import Paddle
from .models import GameState, PlayerState, Event, disable_event, update_game_state

import asyncio
import time

class OnlineGame:

    def __init__(self):
        print("starting online game __init__")
        self.state = GameState()
        self.players = {}

        self._is_rollling = False

        self._paddle_fire_event = Event()
        self._reached_border_event = Event()

        self._paddle_left = Paddle(True, self._paddle_fire_event)
        self._paddle_right = Paddle(False, self._paddle_fire_event)
        self._ball = Ball(self._reached_border_event)
        self._assignable_paddles = {self._paddle_left, self._paddle_right}
        self._paddles = [self._paddle_left, self._paddle_right]


        self._game_loop_timestamp = time.perf_counter_ns() // 1_000_000
        self._state_update_timestamp = time.perf_counter_ns() // 1_000_000
        self._state_update_timestep = 16
        self._time_slept = 0

        print("game initalized")

    def add_player(self, id):
        if id not in self.players:
            self.players[id] = PlayerState(is_controlling=self._assign_paddle())

    def remove_player(self, id):
        if id in self.players:
            paddle = self.players[id].is_controlling
            self._unassign_paddle(paddle)
            del self.players[id]

    def _assign_paddle(self):
        if self._assignable_paddles:
            return self._assignable_paddles.pop()

    def _unassign_paddle(self, paddle):
        self._assignable_paddles.add(paddle)

    async def start(self):
        print("starting")
        while True:
            await self._iterate()

    async def _iterate(self):
        if self._paddle_fire_event["is_active"]:
            if (
                not self._ball.is_rolling and 
                self._paddle_fire_event.is_left == self._ball.is_left
            ):
                self._ball.launch()
                self._ball.is_rolling = True
            disable_event(self._paddle_fire_event)

        if self._reached_border_event["is_active"]:
            if self._reached_border_event.is_left: 
                self._paddle_right.score += 1
            else: 
                self._paddle_left.score += 1
            self._ball.reset(self._reached_border_event.is_left)
            disable_event(self._reached_border_event)

        frame_time = (time.perf_counter_ns() // 1_000_000) - self._game_loop_timestamp - self._time_slept
        self._game_loop_timestamp = time.perf_counter_ns() // 1_000_000
        dt = frame_time / 1000 * 60

        for player in self.players.values():
            player["is_controlling"].update(player["inputs"], dt)
        self._ball.update(
            dt, self._paddle_left.rect.center if self._ball._is_left else self._paddle_right.rect.center, self._paddles
        )

        if (time.perf_counter_ns() // 1_000_000) - self._state_update_timestamp >= self._state_update_timestep:
            update_game_state(self.state, self._paddle_left, self._paddle_right, self._ball)
            self._state_update_timestamp = time.perf_counter_ns() // 1_000_000

        self._time_slept = max(0, 1 / 60 * 1000 - frame_time)
        await asyncio.sleep(self._time_slept // 1000)