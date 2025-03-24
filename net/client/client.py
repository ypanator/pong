import asyncio
from queue import Queue
import socket
import threading
import json

import pygame

class Client:

    def __init__(self):
        self._loop = None
        self._thread = None
        self._host = "127.0.0.1"
        self._port = 8888
        self._writer = None
        self._reader = None
        self.connected = False
        self._msg_queue = Queue()
    
    def connect(self):
        if self.connected:
            return True
            
        self._thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self._thread.start()
        
        # Wait for connection with timeout
        start_time = pygame.time.get_ticks()
        while not self.connected:
            if pygame.time.get_ticks() - start_time > 5000:  # 5 second timeout
                return False
            pygame.time.wait(100)  # Small delay to prevent CPU spinning
        return True
    
    def _start_event_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._async_connect())
    
    async def _async_connect(self):
        try:
            self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
            self.connected = True
            await self._receive_loop()
        except (ConnectionRefusedError, socket.error) as e:
            print(f"Connection error: {e}")

    async def _receive_loop(self):
        try:
            while True:
                data = await self._reader.readline()
                if not data:
                    self.connected = False
                    break
                self._msg_queue.put(json.loads(data.decode()))
        except asyncio.CancelledError as e:
            print(e)
            pass
    
    async def _async_write(self, message):
        if not self._writer or self._writer.is_closing():
            raise ConnectionError("Not connected to server")        
        self._writer.write((json.dumps(message) + "\n").encode())
        await self._writer.drain()
    
    async def _async_close(self):
        self._writer.close()
        await self._writer.wait_closed()
    
    def close(self):
        if self.connected:
            asyncio.run_coroutine_threadsafe(self._async_close(), self._loop)
            if self._thread and self._thread.is_alive():
                self._thread.join()
            self.connected = False

    def write(self, message):
        if self.connected:
            asyncio.run_coroutine_threadsafe(self._async_write(message), self._loop)
    
    def read(self):
        if not self._msg_queue.empty():
            return self._msg_queue.get_nowait()
        return None