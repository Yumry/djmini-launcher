class Scene(object):
    def __init__(self, launcher):
        self.launcher = launcher

    def start_scene(self):
        pass

    def unload_scene(self):
        self.launcher.window.remove_handlers()
        if self.launcher.controller is not None:
            self.launcher.controller.remove_handlers()

        if self.launcher.native_controller is not None:
            self.launcher.native_controller.remove_handlers()