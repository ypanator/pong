import asyncio
import json
import random
import string
import net.server.server_codes as server_codes
import time
from net.server.client_state import ClientState
from rooms_manager import RoomsManager

rooms_manager = RoomsManager()

async def handle_client(reader, writer):

    print(f"Connection from {writer.get_extra_info('peername')}")

    state = ClientState()
    tasks = []

    timestamp = 0
    timestep = 50

    try:
        while True:
            msg = await reader.readline()
            if not msg:
                break
            msg = json.loads(msg.decode())
            print(f"Received: {msg}")

            tasks.append(asyncio.create_task(handle_msg(msg, state, writer)))

            if state.in_room() and rooms_manager.is_broadcaster(state.room_code, writer):
                if time.monotonic() - timestamp >= timestep and state.game_state.is_updated:
                    timestamp = time.monotonic()
                    tasks.append(asyncio.create_task(broadcast_game(state.writers, state.game_state)))

        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        code = state.leave_room()

        # if the last client left the room, delete it
        if code is not None and rooms_manager.is_empty(code):
            rooms_manager.remove_room(code)

        writer.close()
        await writer.wait_closed()

async def handle_msg(msg, state, writer):
    if not isinstance(msg, dict) or not "type" in msg or not "data" in msg: 
        await write(writer, server_codes.ERROR, "Incorrect message format.")
        return

    type = msg["type"]
    if type == server_codes.JOIN_REQ:
        code = msg["data"]
        if not isinstance(code, str) or len(code) != 5 or not code.isalpha():
            await write(writer, server_codes.ERROR, "Incorrect room code.")
            return
        if not rooms_manager.exists(code):
            await write(writer, server_codes.ERROR, "Room does not exist.")
            return
        if rooms[]
        
        code = code.lower()
        state.join_room()
        rooms[code].add(writer)

        await write(writer, server_codes.ROOM_JOIN, f"Joined room: {code}")

    elif type == server_codes.CREATE_REQ:
        code = await generate_code()
        room_init(code)
        rooms[code] = {writer}
        state.room = code

        await write(writer, server_codes.ROOM_CREATE, f"Created and joined room: {code}")

    elif type == server_codes.SEND_POS_REQ:
        pos = msg["data"]
        if not isinstance(pos, list) or len(pos) != 2 or not isinstance(pos[0], int) or not isinstance(pos[1], int):
            await write(writer, server_codes.ERROR, "Incorrect position format.")
            return
        if state.room is None:
            await write(writer, server_codes.ERROR, "Not connected to a room.")
            return
        for wrt in rooms[state.room]:
            if wrt == writer:
                continue
            await write(wrt, server_codes.POS_UPDATE, pos)
        
        await write(writer, server_codes.POS_SEND, f"Position sent: {pos[0]} {pos[1]}")
    
    elif type == server_codes.GET_CODE_REQ:
        await write(writer, server_codes.ROOM_CODE, state.room)

    else:
        await write(writer, server_codes.ERROR, "Incorrect type provided.")
        return

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    print("Successfuly started serving on 127.0.0.1:8888")
    async with server:
        await server.serve_forever()

async def write(writer, type, data):
    writer.write((json.dumps({"type": type, "data": data}) + "\n").encode())
    await writer.drain()

async def broadcast_game(writers, game):
    pass # TODO:

def room_init(code):
    pass

def generate_code():
    return "".join(random.sample(string.ascii_lowercase, k=6))

asyncio.run(main())