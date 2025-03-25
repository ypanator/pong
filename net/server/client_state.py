class ClientState:
    def __init__(self):
        self.room_code = None
        self.game = None
    
    @property
    def in_room(self):
        return self.room_code is not None and self.game is not None
    
    def join_room(self, code, rooms):
        self.room_code = code
        self.game = self.room_ref["game"]
    
    def leave_room(self):
        code = None
        if self.in_room:
            code = self.room_code
            self.room_code = None
            self.game = None
        return code