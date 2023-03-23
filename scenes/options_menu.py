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
                           font_name='Arial',
                           font_size=config.get_config()['font_size'] * util.SCALE_FACTOR,
                           x=util.scale_x(512), y=util.scale_y(700),
                           anchor_x='center', anchor_y='center')

        self.option_list = UITextList(util.scale_x(110), util.scale_y(600), util.scale_x(804))
        self.option_list.append_entry('Back', Action.BACK)

        self.option_bindings = UITextList(util.scale_x(110), util.scale_y(600), 
                               util.scale_x(804), self.option_list)
        self.option_bindings.append_entry('Back', Action.BACK)
        for binding in config.get_config()['key_bindings']:
            self.option_bindings.append_entry(binding + ' : ', Action.KEYBIND, binding)

        self.option_list.append_entry('Button Bindings', Action.CATEGORY, self.option_bindings)

        self.active_menu = self.option_list
        self.binding_popup = UIPopUp('Waiting for input...')


        self.launcher.window.set_handler('on_draw', self.on_draw)
        self.launcher.window.set_handler('on_key_press', self.on_key_press)
        if(self.launcher.controller is not None):
            self.launcher.controller.set_handler('on_button_press', self.on_button_press)
            self.launcher.controller.set_handler('on_dpad_motion', self.on_dpad_motion)

    def on_draw(self):
        self.launcher.window.clear()
        self.rect_bg.draw()
        self.label_title.draw()
        self.active_menu.draw()
        if self.in_popup:
            self.binding_popup.draw()

    def start_press(self):
        match self.active_menu.get_selection().action:
            case Action.BACK:
                if self.active_menu.parent == None:
                    self.launcher.load_scene()
                else: self.active_menu = self.active_menu.parent
            case Action.KEYBIND:
                self.in_popup = True
            case Action.CATEGORY:
                pass
                self.active_menu = self.active_menu.get_selection().input

    def delete_input(self):
        if self.active_menu.get_selection().action == Action.KEYBIND:
            config.bindings[self.active_menu.get_selection().input] = []
            config.save_config()

    def save_input(self, symbol):
        config.bindings[self.active_menu.get_selection().input].append(symbol)
        config.save_config()
        self.in_popup = False

    def on_input(self, symbol):
        if not self.in_popup:
            if symbol in config.bindings['settings']:
                self.launcher.unload_scene()
                self.launcher.load_scene()
            if symbol in config.bindings['down']:
                self.active_menu.set_selection(self.active_menu.selected + 1)
            if symbol in config.bindings['up']:
                self.active_menu.set_selection(self.active_menu.selected - 1)
            if symbol in config.bindings['start']:
                self.start_press()
            if symbol in config.bindings['delete']:
                self.delete_input()
        # Keybinding popup is running. Let's set our keybind
        else:
            self.save_input(symbol)

    def on_key_press(self, symbol, modifiers):
        self.on_input(symbol)
    
    def on_button_press(self, controller, pressed_button):
        button = 'btn_' + pressed_button
        self.on_input(button)

    def on_dpad_motion(self, controller, left, right, up, down):
        if left:
            self.on_input('dpad_l')
        if right:
            self.on_input('dpad_r')
        if up:
            self.on_input('dpad_u')
        if down:
            self.on_input('dpad_d')
