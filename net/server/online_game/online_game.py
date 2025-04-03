from entities import Ball, Paddle
from models import GameState, PlayerState, Event

import asyncio
import time

class OnlineGame:

    def __init__(self):
        self.state = GameState()
        self._players = {}

        self._is_rollling = False

        self._paddle_left = Paddle(True)
        self._paddle_right = Paddle(False)
        self._ball = Ball()
        self._assignable_paddles = {self._paddle_left, self._paddle_right}
        self._paddles = [self._paddle_left, self._paddle_right]

        self._paddle_fire_event = Event()
        self._reached_border_event = Event()

        self._game_loop_timestamp = time.perf_counter_ns() // 1_000_000
        self._state_update_timestamp = time.perf_counter_ns() // 1_000_000
        self._state_update_timestep = 50
        self._time_slept = 0

    def add_player(self, id):
        if id not in self._players:
            self._players[id] = PlayerState(is_controlling=self._assign_paddle())

    def remove_player(self, id):
        if id in self._players:
            paddle = self._players[id].is_controlling
            self._unassign_paddle(paddle)
            del self._players[id]

    def _assign_paddle(self):
        if self._assignable_paddles:
            return self._assignable_paddles.pop()

    def _unassign_paddle(self, paddle):
        self._assignable_paddles.add(paddle)

    async def start(self):
        while True:
            await self._iterate()

    async def _iterate(self):
        if self._paddle_fire_event.is_active:
            if (
                not self._ball.is_rolling and 
                self._paddle_fire_event.is_left == self._ball.is_left
            ):
                self._ball.launch()
                self._ball.is_rolling = True

        if self._reached_border_event.is_active:
            if self._reached_border_event.is_left: 
                self._paddle_right.score += 1
            else: 
                self._paddle_left.score += 1
            self._ball.reset(self._reached_border_event.is_left)

        time = (time.perf_counter_ns() // 1_000_000) - self._game_loop_timestamp - self._time_slept
        self._game_loop_timestamp = time.perf_counter_ns() // 1_000_000
        dt = time / 1000 * 60

        for player in self._players.values():
            player.is_controlling.update(player.inputs, dt)
        self._ball.update(
            dt, self._paddle_left.rect.center if self._ball.is_left else self._paddle_right.rect.center, self._paddles
        )

        if (time.perf_counter_ns() // 1_000_000) - self._state_update_timestamp >= self._state_update_timestep:
            self.state.update(self._paddle_left, self._paddle_right, self._ball)
            self._state_update_timestamp = time.perf_counter_ns() // 1_000_000

        self._time_slept = max(0, 1 / 60 * 1000 - time)
        await asyncio.sleep(self._time_slept // 1000)