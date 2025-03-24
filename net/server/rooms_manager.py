import asyncio

class RoomsManager:

    def __init__(self):
        # room_id: {"writers": [writers], "game": (OnlineGame, game_task)}
        self._rooms = {}
        self._locks = {}
    
    def _get_lock(self, room_code):
        if room_code not in self._locks:
            self._locks[room_code] = asyncio.Lock()
        return self._locks[room_code]

    async def room_init(self, room_code, writer):
        async with self._get_lock(room_code):
            pass

    async def remove_room(self, room_code):
        async with self._get_lock(room_code):
            pass

    async def join_room(self, room_code, writer):
        async with self._get_lock(room_code):
            pass

    async def leave_room(self, room_code, writer):
        async with self._get_lock(room_code):
            writers = self._rooms[room_code]["writers"]
            if writer in writers:
                self._rooms[room_code]["writers"].remove(writer)
        
    async def is_empty(self, room_code):
        async with self._get_lock(room_code):
            return not self._rooms[room_code]["writers"]
        
    async def is_full(self, room_code):
        async with self._get_lock(room_code):
            return len(self._rooms[room_code]["writers"]) >= 2
        
    async def get_game(self, room_code):
        async with self._get_lock(room_code):
            return self._rooms[room_code]["game"][0]
        
    async def is_broadcaster(self, room_code, writer):
        async with self._get_lock(room_code):
            writers = self._rooms[room_code]["writers"]
            return writer in writers and writer == writers[0] 