import pyglet
import bmlauncher.config as config
from scenes.main_menu import MainMenu
from scenes.options_menu import OptionsMenu
from bmlauncher.native_controller import Controller

config.initialize()
WIDTH = config.get_config()['resolution_x']
HEIGHT = config.get_config()['resolution_y']

class Launcher(object):
    def __init__(self):
        self.current_scene = MainMenu(self)
        self.controller = None
        self.controllers = pyglet.input.get_controllers()
        if self.controllers:
            print('Connecting to controller', self.controllers[0].name)
            self.controller = self.controllers[0]
            self.controllers[0].open()
        
        self.native_controller = None
        if config.get_config()['native_linux_joysticks']:
            self.native_controller = Controller(config.get_config()['native_joystick_device'])
            self.native_controller.daemon = True
            self.native_controller.start()

    def start_scene(self):
        self.current_scene.start_scene()

    def execute(self):
        self.window = pyglet.window.Window(WIDTH, HEIGHT)
        self.window.set_vsync(config.get_config()['enable_vsync'])
        self.window.set_exclusive_mouse(True)

        self.load_scene()
        pyglet.app.run(interval=1/config.get_config()['fps_limit'])
    
    def unload_scene(self):
        if self.current_scene is not None:
            self.current_scene.unload_scene()

    def load_scene(self, scene=MainMenu):
        self.current_scene = scene(self)
        self.start_scene()

    def shutdown(self):
        # once the program is exiting close the controller thread
        if self.native_controller is not None:
            self.native_controller.stop()



launcher = Launcher()
launcher.execute()
launcher.shutdown()