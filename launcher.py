import pyglet
import bmlauncher.config as config
from scenes.main_menu import MainMenu
from scenes.options_menu import OptionsMenu

config.initialize()
WIDTH = config.get_config()['resolution_x']
HEIGHT = config.get_config()['resolution_y']

class Launcher(object):
    def __init__(self):
        self.current_scene = MainMenu(self)

    def start_scene(self):
        self.current_scene.start_scene()

    def execute(self):
        self.window = pyglet.window.Window(WIDTH, HEIGHT)
        self.window.set_exclusive_mouse(True)
        self.start_scene()
        pyglet.app.run()
    
    def unload_scene(self):
        if self.current_scene is not None:
            self.current_scene.unload_scene()
    
    def load_scene(self, scene=MainMenu):
        self.unload_scene()
        self.current_scene = scene(self)
        self.start_scene()
    

launcher = Launcher()
launcher.execute()