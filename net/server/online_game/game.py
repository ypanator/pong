import asyncio
from entities import Ball, Player

"""
================= self.state =================
"players": list({
    "is_left": bool
    "x": int, "y": int 
})
"ball": {
    "x": int, "y": int,
    "xv": int, "yv": int,
    "vel": int
}

================= self.players =================
player_id: {
    "is_controlling": paddle, 
    "inputs": {
        "UP": bool, 
        "DOWN": bool, 
        "FIRE": bool
    }
}
"""

class OnlineGame:

    def __init__(self):
        self.state = {
            "players": list(),
            "ball": {
                "x": -1, "y": -1, "xv": -1, "yv": -1, "vel": -1
            }
        }
        self._players = {}

        self._running = False

        # TODO: initalize game stuffs
        self._player_left = Player(True)
        self._player_right = Player(False)
        self._ball = Ball()
        self._paddles = set(self._player_left, self._player_right)

    def add_player(self, id):
        self._players[id] = {
            "is_controlling": self._assign_paddle(), 
            "inputs": {
                "UP": False,
                "DOWN": False, 
                "FIRE": False
            }
        }

    def remove_player(self, id):
        if id in self._players:
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