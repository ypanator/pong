import pygame
import os
import logging
import datetime
import time

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class LoadingScene:

    # state codes
    LOADING = 0
    ERROR = 1

    logger = logging.getLogger(__name__)

    def __init__(self, scene_manager):
        self._screen = pygame.display.get_surface()
        self._scene_manager = scene_manager

        self._changed = True
        self._state = self.LOADING

        self._timestamp = pygame.time.get_ticks()
        self._time_window = 10 * 1000
        self._timestep = 1000

        self._continue = self._get("continue")
        self._previous_scene = self._get("previous_scene")
        self._on_load = self._get("on_load")

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
        if self._state == self.LOADING:
            self._state = self.ERROR
            self._changed = True
            self._timestamp = pygame.time.get_ticks()
        self._info = str(error)
        self.logger.exception(error)

    def iterate(self, ticks):
        print(self._state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._scene_manager.close()

        if self._state == self.LOADING:

            if pygame.time.get_ticks() - self._timestamp > self._time_window:
                self._handle_error(Exception("Loading time exceeded."))
                return
            
            if self._continue():
                self.logger.info("Succesfuly loaded.")
                self._on_load()
                return

        if self._state == self.ERROR:
            if pygame.time.get_ticks() - self._timestamp > self._time_window:
                self._previous_scene()
                self.logger.info("Returning due to an error")
                return

        # if self._changed:
        self._surf = self._font.render(self._info, False, "white", "black")
        self._rect = self._surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self._screen.fill("black")
        self._screen.blit(self._surf, self._rect)

        pygame.display.flip()

        self._changed = False