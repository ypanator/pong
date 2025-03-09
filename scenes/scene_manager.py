class SceneManager:

    # scenes = {scene_name: scene_constructor}
    def __init__(self, scenes):
        self.scenes_classes = scenes
        self.scenes_objects = {}
        self.run = True
    
    def start(self, scene, data):
        if scene not in self.scenes_classes:
            raise ValueError(f"Scene '{scene}' does not exist.")
        
        if self.scenes_objects.get(scene) is None:
            self.scenes_objects[scene] = self.scenes_classes[scene]()

        self.scenes_objects[scene].start(data, self)
    
    def restart_scene(self, scene):
        if scene not in self.scenes_classes:
            raise ValueError(f"Scene '{scene}' does not exist.")
        
        self.scenes_objects[scene] = self.scenes_classes[scene]()