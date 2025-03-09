import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

from scenes.scene_manager import SceneManager
from scenes.game_scene import GameScene

pygame.init()
pygame.display.set_caption("pong")
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scenes = {
    "GameScene": GameScene
}
scene_manager = SceneManager(scenes)
scene_manager.start("GameScene", None)

pygame.quit()