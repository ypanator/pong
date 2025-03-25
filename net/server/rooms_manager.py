import asyncio
from online_game import GameState, run_game

def _locked(func):
    async def wrapper(self, room_code, *args, **kwargs):
        async with self._get_lock(room_code):
            if room_code in self._rooms:
                return await func(self, room_code, *args, **kwargs)
    return wrapper

class RoomsManager:

    def __init__(self):
        # room_id: {"writers": [writers], "game": (GameState, game_task)}
        self._rooms = {}
        self._locks = {}
    
    def _get_lock(self, room_code):
        if room_code not in self._locks:
            self._locks[room_code] = asyncio.Lock()
        return self._locks[room_code]
    
    async def room_init(self, room_code):
        async with self._get_lock(room_code):
            if not room_code in self._rooms:
                state = GameState()
                self._rooms[room_code] = {"writers": [], "game": (state, asyncio.create_task(run_game(state)))}
    @_locked
    async def remove_room(self, room_code):
        del self._rooms[room_code]
    
    @_locked
    async def join_room(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        if len(writers) < 2:
            writers.append(writer)
    
    @_locked
    async def leave_room(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        if writer in writers:
            self._rooms[room_code]["writers"].remove(writer)
    
    @_locked    
    async def is_empty(self, room_code):
        return not self._rooms[room_code]["writers"]
    
    @_locked    
    async def is_full(self, room_code):
        return len(self._rooms[room_code]["writers"]) >= 2
    
    @_locked    
    async def get_game(self, room_code):
        return self._rooms[room_code]["game"][0]

    @_locked 
    async def is_broadcaster(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        return writer in writers and writer == writers[0]
    
    @_locked
    async def get_writers(self, room_code):
        return self._rooms[room_code]["writers"]