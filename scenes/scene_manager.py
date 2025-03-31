import pygame

class SceneManager:

    # scenes = {scene_name: scene_constructor}
    def __init__(self, scenes, first_scene):
        self._scene_classes = scenes
        self._scene_objects = {}

        self._current_scene = first_scene
        self._next_scene = first_scene

        self._clock = pygame.time.Clock()

        self.context = {"clock": self._clock}
        self._run = True

    def start(self):
        while self._run:

            self._current_scene = self._next_scene

            if self._current_scene not in self._scene_classes:
                raise ValueError(f"Scene '{self._current_scene}' does not exist.")
        
            if self._current_scene not in self._scene_objects:
                self._scene_objects[self._current_scene] = self._scene_classes[self._current_scene](self)
            scene_object = self._scene_objects[self._current_scene]

            while self._current_scene == self._next_scene and self._run:
                scene_object.iterate(self._clock.tick())
    
    def restart_scene(self, scene):
        if scene not in self._scene_classes:
            raise ValueError(f"Scene '{scene}' does not exist.")
        
        self._scene_objects[scene] = self._scene_classes[scene](self)
    
    def change_scene(self, scene):
        self._next_scene = scene
    
    def close(self):
        self._run = False