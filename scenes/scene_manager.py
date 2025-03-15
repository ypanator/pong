import pygame

class SceneManager:

    # scenes = {scene_name: scene_constructor}
    def __init__(self, scenes, first_scene):
        self.scene_classes = scenes
        self.scene_objects = {}

        self.current_scene = first_scene
        self.next_scene = first_scene

        self.context = {}
        self.run = True

        self.clock = pygame.time.Clock()
    
    def start(self):
        while self.run:

            self.current_scene = self.next_scene

            if self.current_scene not in self.scene_classes:
                raise ValueError(f"Scene '{self.current_scene}' does not exist.")
        
            if self.current_scene not in self.scene_objects:
                self.scene_objects[self.current_scene] = self.scene_classes[self.current_scene](self)
            scene_object = self.scene_objects[self.current_scene]

            while self.current_scene == self.next_scene and self.run:
                scene_object.iterate(self.clock.tick())
    
    def restart_scene(self, scene):
        if scene not in self.scene_classes:
            raise ValueError(f"Scene '{scene}' does not exist.")
        
        self.scene_objects[scene] = self.scene_classes[scene](self)
    
    def change_scene(self, scene):
        self.next_scene = scene
    
    def close(self):
        self.run = False