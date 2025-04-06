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

    broadcaster_timestamp = 0
    broadcaster_timestep = 50

    try:
        while True:
            msg = await reader.readline()
            if not msg:
                break
            msg = json.loads(msg.decode())
            print(f"Received: {msg}")

            tasks.append(asyncio.create_task(handle_msg(msg, state, writer)))

            if state.in_room() and rooms_manager.is_broadcaster(state.room_code, writer):
                if time.monotonic() - broadcaster_timestamp >= broadcaster_timestep and state.game_state.is_updated:
                    broadcaster_timestamp = time.monotonic()
                    tasks.append(asyncio.create_task(broadcast_state(state.writers, state.game_state)))

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
        room_code = msg["data"]
        if state.in_room():
            await write(writer, server_codes.ERROR, "User already in room.")
            return            
        if not isinstance(room_code, str) or len(room_code) != 6 or not room_code.isalpha() and room_code.islower():
            await write(writer, server_codes.ERROR, "Incorrect room code.")
            return
        if not rooms_manager.exists(room_code):
            await write(writer, server_codes.ERROR, "Room does not exist.")
            return
        if rooms_manager.is_full(room_code):
            await write(writer, server_codes.ERROR, "Room is full.")
            return
                
        state.join_room(room_code, rooms_manager)
        rooms_manager.join_room(room_code, writer)

        await write(writer, server_codes.ROOM_JOINED, f"Joined room: {room_code}")

    elif type == server_codes.CREATE_REQ:
        if state.in_room():
            await write(writer, server_codes.ERROR, "User already in room.")
            return  
        room_code = generate_code()
        await rooms_manager.room_init(room_code)
        rooms_manager.join_room(room_code, writer)
        state.join_room(room_code, rooms_manager)

        await write(writer, server_codes.ROOM_CREATE, f"Created and joined room: {room_code}")

    elif type == server_codes.NEW_INPUTS:
        inputs = msg["data"]
        if (
            not isinstance(inputs, dict) or "up" not in inputs or "down" not in inputs or "fire" not in inputs or
            not isinstance(inputs["up"], bool) or not isinstance(inputs["down"], bool) or not isinstance(inputs["fire"], bool)
        ):
            await write(writer, server_codes.ERROR, "Incorrect position format.")
            return
        if not state.in_room():
            await write(writer, server_codes.ERROR, "User is not connected to a room.")
            return

        # TODO: update player inputs in respective game in room
        pass
        
        await write(writer, server_codes.POS_SEND, f"Position received.")
    
    elif type == server_codes.LEAVE_REQ:
        # TODO: implement leaving the room logic
        pass

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

async def broadcast_state(writers, state):
    for writer in writers:
        await write(writer, server_codes.NEW_STATE, state)

def generate_code():
    return "".join(random.choices(string.ascii_lowercase, k=6))

asyncio.run(main())