from entities import Ball, Paddle
from models import GameState, PlayerState, Event

class OnlineGame:

    def __init__(self):
        self.state = GameState()
        self._players = {}

        self._running = False

        self._player_left = Paddle(True)
        self._player_right = Paddle(False)
        self._ball = Ball()
        self._paddles = set(self._player_left, self._player_right)

        self._paddle_fire_event = Event()
        self._reached_border_event = Event()

    def add_player(self, id):
        if id not in self._players:
            self._players[id] = PlayerState(is_controlling=self._assign_paddle)

    def remove_player(self, id):
        if id in self._players:
            paddle = self._players[id]
            self._unassign_paddle(paddle)
            del self._players[id]

    def _assign_paddle(self):
        if self._paddles:
            return self._paddles.pop()

    def _unassign_paddle(self, paddle):
        self._paddles.add(paddle)

    async def start(self):
        while True:
            await self._iterate()

    async def _iterate(self):
        pass
    """
    time = clock.tick() - time_slept
    dt = time / 1000 * 60
    update(dt)
    time_slept = max(0, 1 / 60 * 1000 - time)
    asyncio.sleep(time_slept)
    """