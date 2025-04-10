import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

from scenes.scene_manager import SceneManager
from scenes.game.local_game_scene import LocalGameScene
from scenes.game.online_game_scene import OnlineGameScene
from scenes.main_menu_scene import MainMenuScene
from scenes.online_menu_scene import OnlineMenuScene
from scenes.loading_scene import LoadingScene

import logging
import os
from datetime import datetime

# ================ logger setup ================
log_dir = os.path.join(os.path.expanduser("~"), "pong_logs")
os.makedirs(log_dir, exist_ok=True)
file_name = f"app_{datetime.now().strftime('%H-%M-%d-%m-%Y')}.log"
log_file = os.path.join(log_dir, file_name)

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================ pygame setup ================
pygame.init()
pygame.font.init()
pygame.display.set_caption("pong")
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scenes = {
    "LocalGameScene": LocalGameScene,
    "MainMenuScene": MainMenuScene,
    "OnlineMenuScene": OnlineMenuScene,
    "LoadingScene": LoadingScene,
    "OnlineGameScene": OnlineGameScene
}
scene_manager = SceneManager(scenes, "MainMenuScene")

try:
    scene_manager.start()
except Exception as e:
    logging.exception(e)

pygame.quit()