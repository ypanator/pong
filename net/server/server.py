import asyncio
import json
import random
import string
import net.server.server_codes as server_codes
import time
from .client_state import ClientState
from .rooms_manager import RoomsManager

rooms_manager = RoomsManager()

async def handle_client(reader, writer):

    print(f"Connection from {writer.get_extra_info('peername')}")

    state = ClientState()
    tasks = []

    broadcaster_timestamp = 0
    broadcaster_timestep = 0.016

    try:
        while True:
            print("waiting for msg")
            msg = await reader.readline()
            if not msg:
                break
            msg = json.loads(msg.decode())
            print(f"Received: {msg}")

            # Process message first
            tasks.append(asyncio.create_task(handle_msg(msg, state, writer)))

            # Then check if we should broadcast state
            if state.in_room() and rooms_manager.is_broadcaster(state.room_code, writer):
                curr_time = time.monotonic()
                if curr_time - broadcaster_timestamp >= broadcaster_timestep:
                    broadcaster_timestamp = curr_time
                    print("Broadcasting state")  # Add debug print
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
                
        join_room(room_code, rooms_manager, writer, state)

        await write(writer, server_codes.ROOM_JOINED, f"Joined room: {room_code}")

    elif type == server_codes.CREATE_REQ:
        print("creating room")
        if state.in_room():
            await write(writer, server_codes.ERROR, "User already in room.")
            print("User already in room.")
            return
        
        room_code = generate_code()
        print("code generated")
        
        # Create and initialize the room first
        await rooms_manager.room_init(room_code)
        print("room init finished")
        
        # Then join the room and notify client
        join_room(room_code, rooms_manager, writer, state)
        print("room joined")
        
        await write(writer, server_codes.ROOM_CREATED, f"Created and joined room: {room_code}")

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

        state.game_coro.players[id(writer)]["inputs"] = inputs
        
        await write(writer, server_codes.POS_SEND, "Position received.")
    
    elif type == server_codes.LEAVE_REQ:
        if not state.in_room():
            await write(writer, server_codes.ERROR, "User is not connected to a room.")
            return
        leave_room(state.room_code, rooms_manager, writer, state)

        await write(writer, server_codes.ROOM_LEFT, "User left the room.")

    elif type == server_codes.GET_CODE_REQ:
        if not state.in_room():
            await write(writer, server_codes.ERROR, "User is not connected to a room.")
            return    
            
        await write(writer, server_codes.ROOM_CODE, state.room_code)

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
    print(f"successfully sent {{'type': {type}, 'data': {data}}}")
    await writer.drain()

async def broadcast_state(writers, state):
    for writer in writers:
        await write(writer, server_codes.NEW_STATE, state)

def join_room(room_code, rooms_manager, writer, state):
    rooms_manager.join_room(room_code, writer)
    state.join_room(room_code, rooms_manager)
    state.game_coro.add_player(id(writer))

def leave_room(room_code, rooms_manager, writer, state):
    rooms_manager.leave_room(room_code, writer)
    state.leave_room()
    state.game_coro.remove_player(id(writer))

def generate_code():
    return "".join(random.choices(string.ascii_lowercase, k=6))

asyncio.run(main())