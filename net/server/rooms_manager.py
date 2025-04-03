import asyncio
from net.server.online_game.online_game import OnlineGame
from net.server.online_game.models import GameState
from dataclasses import dataclass, field


@dataclass
class Room:
    @dataclass
    class GameData:
        coro: OnlineGame = field(default_factory=OnlineGame)
        state: GameState = field(init=False)

        def __post_init__(self):
            self.state = self.coro.state

    game: GameData = field(default_factory=GameData)
    writers: list[asyncio.StreamWriter] = field(default_factory=list)

class RoomsManager:

    def __init__(self):
        self._rooms = {}
    
    async def room_init(self, room_code):
        if not room_code in self._rooms:
            self._rooms[room_code] = Room()
            await self._rooms[room_code].game.coro.start()

    def remove_room(self, room_code):
        del self._rooms[room_code]
    
    def join_room(self, room_code, writer):
        writers = self._rooms[room_code].writers
        # could be deleted to allow spectators?
        if len(writers) < 2:
            writers.append(writer)
    
    def leave_room(self, room_code, writer):
        writers = self._rooms[room_code].writers
        if writer in writers:
            writers.remove(writer)
        
    def is_empty(self, room_code):
        return not self._rooms[room_code].writers
        
    def is_full(self, room_code):
        return len(self._rooms[room_code].writers) >= 2
        
    def get_game_coro(self, room_code):
        return self._rooms[room_code].game.coro

    def get_game_state(self, room_code):
        return self._rooms[room_code].game.state
 
    def is_broadcaster(self, room_code, writer):
        writers = self._rooms[room_code].writers
        return writer in writers and writer == writers[0]
    
    def get_writers(self, room_code):
        return self._rooms[room_code].writers
    
    def exists(self, room_code):
        return room_code in self._rooms