class Scene(object):
    def __init__(self, launcher):
        self.launcher = launcher

    def start_scene(self):
        pass

    def unload_scene(self):
        self.launcher.window.remove_handlers()