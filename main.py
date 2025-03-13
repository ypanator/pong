import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

from scenes.scene_manager import SceneManager
from scenes.local_game_scene import LocalGameScene
from scenes.main_menu_scene import MainMenuScene

pygame.init()
pygame.display.set_caption("pong")
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scenes = {
    "LocalGameScene": LocalGameScene,
    "MainMenuScene": MainMenuScene
}
scene_manager = SceneManager(scenes, "MainMenuScene")
scene_manager.start()

pygame.quit()