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

        self.state_lock = asyncio.Lock()
        self._player_locks = {}
        self._paddles_lock = asyncio.Lock()

        self._running = False

        # TODO: initalize game stuffs
        self._player_left = Player(True)
        self._player_right = Player(False)
        self._ball = Ball()
    
    def _get_player_lock(self, id):
        if id not in self._player_locks:
            self._player_locks[id] = asyncio.Lock()
        return self._player_locks[id]

    async def add_player(self, id):
        async with self._get_player_lock(id):
            self._players[id] = {
                "is_controlling": self._assign_paddle(), 
                "inputs": {
                    "UP": False,
                    "DOWN": False, 
                    "FIRE": False
                }
            }

    async def remove_player(self, id):
        async with self._get_player_lock(id):
            if id in self._players:
                del self._players[id]

    def _assign_paddle():
        pass

    def _unassign_paddle():
        pass

    def _iterate(self):
        pass

    def start():
        pass # TODO: iterate in a loop