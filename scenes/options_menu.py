import pyglet
import bmlauncher.util as util
from scenes.scene import Scene
from pyglet.window import key


class OptionsMenu(Scene):
    def start_scene(self):
        self.label_title = pyglet.text.Label('Options Menu',
                                font_name='Arial',
                                font_size=50 * util.SCALE_FACTOR,
                                x=util.scale_x(512), y = util.scale_y(700),
                                anchor_x='center', anchor_y='center')

        self.launcher.window.set_handler('on_draw', self.on_draw)
        self.launcher.window.set_handler('on_key_press', self.on_key_press)

    def on_draw(self):
        self.launcher.window.clear()
        self.label_title.draw()
    
    def on_key_press(self, symbol, modifiers):
        if(symbol == key.SPACE):
            self.launcher.load_scene()