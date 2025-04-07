import pygame
import logging
from net.client.client import Client

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class LoadingScene:

    # state codes
    CONNECTING = 0
    AWAIT_SUCCESS = 1
    ERROR = 2

    logger = logging.getLogger(__name__)

    def __init__(self, scene_manager):
        self._screen = pygame.display.get_surface()
        self._scene_manager = scene_manager

        if "client" in self._scene_manager.context: 
            self._client = self._scene_manager.context["client"]
        else:
            self._client = Client()
        self._state = self.CONNECTING if self._client.connected else self.AWAIT_SUCCESS
        self._changed = True

        self._success_timestamp = None
        self._success_window = 5 * 1000

        self._connecting_start_timestamp = pygame.time.get_ticks()
        self._connecting_try_timestamp = 0
        self._connecting_try_timestep = 2.5 * 1000
        self._connecting_window = 10 * 1000

        self._on_start = self._get("on_start")
        self._success = self._get("success")
        self._previous_scene = self._get("previous_scene")
        self._on_success = self._get("on_success")


        self._info = "Loading"
        self._font_size = 35

        self._font = pygame.font.Font("retro_font.ttf", self._font_size)

    def _get(self, func):
        try:
            res = self._scene_manager.context["loading"][func]
            assert res is not None
            self.logger.info(f"Successfuly retrieved {func}()")
            return res
        except Exception:
            self._handle_error(Exception(f"Could not load the \"{func}()\" method from global context."))

    def _handle_error(self, error):
        if self._state != self.ERROR:
            self._state = self.ERROR
            self._changed = True
            self._success_timestamp = pygame.time.get_ticks()
        self._info = str(error)
        self.logger.exception(error)

    def iterate(self, ticks):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._scene_manager.close()

        if self._state == self.CONNECTING:
            
            if pygame.time.get_ticks() - self._connecting_start_timestamp > self._connecting_window:
                self._handle_error(Exception("Loading time exceeded."))
                return
            
            if pygame.time.get_ticks() - self._connecting_try_timestamp > self._connecting_try_timestep:
                if self._client.connected:
                    self._on_start()
                    self._state = self.AWAIT_SUCCESS
                    self._success_timestamp = pygame.time.get_ticks()
                    return
                self._connecting_try_timestamp = pygame.time.get_ticks()
                self._client.connect()

        elif self._state == self.AWAIT_SUCCESS:

            if pygame.time.get_ticks() - self._success_timestamp > self._success_window:
                self._handle_error(Exception("Loading time exceeded."))
                return
            
            if self._success():
                self.logger.info("Succesfully loaded.")
                self._on_success()
                return

        elif self._state == self.ERROR:
            if pygame.time.get_ticks() - self._success_timestamp > self._success_window:
                self._previous_scene()
                self.logger.info("Returning due to an error")
                return

        if self._changed:
            self._surf = self._font.render(self._info, False, "white", "black")
            self._rect = self._surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._screen.fill("black")
        self._screen.blit(self._surf, self._rect)

        pygame.display.flip()

        self._changed = False