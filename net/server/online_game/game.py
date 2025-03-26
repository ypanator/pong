import asyncio

class OnlineGame:

    def __init__(self):
        self.state = {

        }
        
        """
        player_id: {
            "is_controlling": paddle, 
            "inputs": {
                "UP": bool, 
                "DOWN": bool, 
                "FIRE": bool
            }
        }
        """
        self.players = {

        }
        self.player_locks = {}
        self.running = False
        # TODO: initalize game stuffs
    
    def _get_lock():
        pass

    def add_player():
        pass

    def remove_player():
        pass

    def _iterate():
        pass

    def start():
        pass # TODO: iterate in a loop