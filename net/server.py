import asyncio
import json
import random
import string

rooms = {} # room_id: writers

async def handle_client(reader, writer):
    state = State()
    tasks = []

    while True:
        msg = await reader.readline()
        if not msg:
            break
        msg = json.loads(msg.decode())

        tasks.append(asyncio.create_task(handle_msg(msg, state, writer)))
    
    await asyncio.gather(*tasks)

    if state.room is not None:
        rooms[state.room].remove(writer)
        if not rooms[state.room]:
            del rooms[state.room]

    writer.close()
    await writer.wait_closed()

async def handle_msg(msg, state, writer):
    if not isinstance(msg, dict) or not "type" in msg or not "data" in msg: 
        await write(writer, "error", "Incorrect message format.")
        return

    match msg["type"]:
        case "join":
            code = msg["data"]
            if len(code) != 5 or not code.isalpha():
                await write(writer, "error", "Incorrect room code.")
                return
            if code not in rooms:
                await write(writer, "error", "Room does not exist.")
                return
            
            code = code.lower()
            state.room = code
            rooms[code].add(writer)

            await write(writer, "ok", f"Joined room: {code}")

        case "create":
            code = generate_code()
            rooms[code] = set(writer)
            state.room = code

            await write(writer, "ok", f"Created and joined room: {code}")

        case "pos":
            pos = msg["data"]
            if not isinstance(pos, list) or len(pos) != 2 or not isinstance(pos[0], int) or not isinstance(pos[1], int):
                await write(writer, "error", "Incorrect position format.")
                return
            if state.room is None:
                await write(writer, "error", "Not connected to a room.")
                return
            for wrt in rooms[state.room]:
                if wrt == writer:
                    continue
                await write(wrt, "pos", pos)
            
            await write(writer, "ok", f"Position sent: {pos[0]} {pos[1]}")

        case _:
            await write(writer, "error", "Incorrect type provided.")
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

def generate_code():
    code = None
    while code is None or code in rooms:
        code = ''.join(random.choices(string.ascii_lowercase, 5))
    return code

asyncio.run(main())