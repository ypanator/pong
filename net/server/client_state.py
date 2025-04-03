class ClientState:
    def __init__(self):
        self.room_code = None
        self.game_coro = None
        self.game_state = None
        self.writers = None
    
    def in_room(self):
        return all(val is not None for val in vars(self).values())
    
    def join_room(self, room_code, rooms_manager):
        self.room_code = room_code
        self.game_coro = rooms_manager.get_game_coro(room_code)
        self.game_state = rooms_manager.get_game_state(room_code)
        self.writers = rooms_manager.get_writers(room_code)
    
    def leave_room(self):
        code = None
        if self.in_room:
            code = self.room_code
            for prop in vars(self).keys():
                setattr(self, prop, None)
        return code