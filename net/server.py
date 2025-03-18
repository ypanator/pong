import asyncio
import json
import random
import string
import net.server_code as codes

rooms = {} # room_id: writers
rooms_lock = asyncio.Lock()

async def handle_client(reader, writer):
    state = State()
    tasks = []

    try:
        while True:
            msg = await reader.readline()
            if not msg:
                break
            msg = json.loads(msg.decode())

            tasks.append(asyncio.create_task(handle_msg(msg, state, writer)))

        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if state.room is not None:
            rooms[state.room].remove(writer)
            if not rooms[state.room]:
                del rooms[state.room]

        writer.close()
        await writer.wait_closed()

async def handle_msg(msg, state, writer):
    if not isinstance(msg, dict) or not "type" in msg or not "data" in msg: 
        await write(writer, codes.ERROR, "Incorrect message format.")
        return

    match msg["type"]:
        case codes.JOIN_REQ:
            code = msg["data"]
            if len(code) != 5 or not code.isalpha():
                await write(writer, codes.ERROR, "Incorrect room code.")
                return
            if code not in rooms:
                await write(writer, codes.ERROR, "Room does not exist.")
                return
            
            code = code.lower()
            state.room = code
            rooms[code].add(writer)

            await write(writer, codes.ROOM_JOIN, f"Joined room: {code}")

        case codes.CREATE_REQ:
            code = await generate_code()
            rooms[code] = {writer}
            state.room = code

            await write(writer, codes.ROOM_CREATE, f"Created and joined room: {code}")

        case codes.SEND_POS_REQ:
            pos = msg["data"]
            if not isinstance(pos, list) or len(pos) != 2 or not isinstance(pos[0], int) or not isinstance(pos[1], int):
                await write(writer, codes.ERROR, "Incorrect position format.")
                return
            if state.room is None:
                await write(writer, codes.ERROR, "Not connected to a room.")
                return
            for wrt in rooms[state.room]:
                if wrt == writer:
                    continue
                await write(wrt, codes.POS_UPDATE, pos)
            
            await write(writer, codes.POS_SEND, f"Position sent: {pos[0]} {pos[1]}")
        
        case codes.GET_CODE_REQ:
            await write(writer, codes.ROOM_CODE, state.room)

        case _:
            await write(writer, codes.ERROR, "Incorrect type provided.")
            return

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()

class State:
    def __init__(self):
        self.room = None

async def write(writer, type, data):
    writer.write((json.dumps({"type": type, "data": data}) + "\n").encode())
    await writer.drain()

async def generate_code():
    async with rooms_lock:
        while True:
            code = ''.join(random.choices(string.ascii_lowercase, k=5))
            if code not in rooms:
                rooms[code] = set()
                return code

asyncio.run(main())