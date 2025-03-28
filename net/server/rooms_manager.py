import asyncio
from online_game import GameState, run_game

class RoomsManager:

    def __init__(self):
        # room_id: {"writers": [writers], "game": (GameState, game_task)}
        self._rooms = {}
    
    def room_init(self, room_code):
        if not room_code in self._rooms:
            state = GameState()
            self._rooms[room_code] = {"writers": [], "game": (state, asyncio.create_task(run_game(state)))}

    def remove_room(self, room_code):
        del self._rooms[room_code]
    
    def join_room(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        if len(writers) < 2:
            writers.append(writer)
    
    def leave_room(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        if writer in writers:
            self._rooms[room_code]["writers"].remove(writer)
        
    def is_empty(self, room_code):
        return not self._rooms[room_code]["writers"]
        
    def is_full(self, room_code):
        return len(self._rooms[room_code]["writers"]) >= 2
        
    def get_game(self, room_code):
        return self._rooms[room_code]["game"][0]
 
    def is_broadcaster(self, room_code, writer):
        writers = self._rooms[room_code]["writers"]
        return writer in writers and writer == writers[0]
    
    def get_writers(self, room_code):
        return self._rooms[room_code]["writers"]