import pyglet
import bmlauncher.util as util
from scenes.scene import Scene
from pyglet.window import key
import pyglet.shapes as shapes
import bmlauncher.config as config
from bmlauncher.ui_text_list import *
from bmlauncher.ui_popup import UIPopUp

class OptionsMenu(Scene):
    def start_scene(self):
        self.in_popup = 0

        self.rect_bg = shapes.Rectangle(util.scale_x(100), util.scale_y(100), 
                        util.scale_x(824), util.scale_y(550), (33, 5, 41))

        self.label_title = pyglet.text.Label('Options Menu',
                                font_name = 'Arial',
                                font_size = config.get_config()['font_size'] * util.SCALE_FACTOR,
                                x = util.scale_x(512), y = util.scale_y(700),
                                anchor_x = 'center', anchor_y = 'center')
        
        self.option_list = UITextList(util.scale_x(110), util.scale_y(600), util.scale_x(804))

        self.option_list.append_entry('Back', Action.BACK)
        self.option_list.append_entry('Keyboard Bindings', Action.CATEGORY)
        for binding in config.get_config()['key_bindings']:
            self.option_list.append_entry(binding + ' : ', Action.KEYBIND, binding)
        
        self.binding_popup = UIPopUp('Waiting for input...')

        self.launcher.window.set_handler('on_draw', self.on_draw)
        self.launcher.window.set_handler('on_key_press', self.on_key_press)

    def on_draw(self):
        self.launcher.window.clear()
        self.rect_bg.draw()
        self.label_title.draw()
        self.option_list.draw()
        if self.in_popup:
            self.binding_popup.draw()
    
    def on_key_press(self, symbol, modifiers):
        if not self.in_popup:
            if symbol == config.bindings['settings']:
                self.launcher.load_scene()
            if symbol == config.bindings['down']:
                self.option_list.set_selection(self.option_list.selected + 1)
            if symbol == config.bindings['up']:
                self.option_list.set_selection(self.option_list.selected - 1)
            if symbol == config.bindings['start']:
                match self.option_list.get_selection().action:
                    case Action.BACK:
                        self.launcher.load_scene()
                    case Action.KEYBIND:
                        self.in_popup = True
        # Keybinding popup is running. Let's set our keybind
        else:
            config.bindings[self.option_list.get_selection().input] = symbol
            config.save_config()
            self.in_popup = False