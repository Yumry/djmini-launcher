import pyglet
from pyglet.window import key
import bmlauncher.util as util
import bmlauncher.ui_scrollable_row as ui_scrollable_row
import bmlauncher.ui_element as ui_element
import bmlauncher.config as config
from scenes.scene import Scene
from scenes.options_menu import OptionsMenu
import subprocess

MOUSE_SENSITIVITY = config.get_config()['mouse_sensitivity']

class MainMenu(Scene):
    def start_scene(self):
        self.panel_top = ui_element.UIElement(
            pyglet.resource.image('assets/panel_top.png'), x=512, y=720)
        
        self.panel_left = ui_element.UIElement(
            pyglet.resource.image('assets/panel_corner.png'), x = 100, y = 50)

        self.panel_right = ui_element.UIElement(
            pyglet.resource.image('assets/panel_corner.png'), x = 924, y = 50)
        self.panel_right.image = self.panel_right.image.get_transform(flip_x = True)

        self.hint_left = ui_element.UIElement(
            pyglet.resource.image('assets/hint_changegame.png'), x = 80, y = 50)
            
        self.hint_right = ui_element.UIElement(
            pyglet.resource.image('assets/hint_startgame.png'), x = 944, y = 50)

        self.records = []

        for i in range(len(config.roms)):
            record_image = pyglet.resource.image('assets/record.png')
            newrecord = ui_scrollable_row.UiScrollableRow(
                i, True, record_image, x=512, y=360)
            self.records.append(newrecord)

        self.label_title = pyglet.text.Label('Unknown ROM',
                                font_name='Arial',
                                font_size=config.get_config()['font_size'] * util.SCALE_FACTOR,
                                x=util.scale_x(512), y = util.scale_y(550),
                                anchor_x='center', anchor_y='center')

        for record in self.records:
            pyglet.clock.schedule_interval(record.update, 0.00005)
        
        self.launcher.window.set_handler('on_draw', self.on_draw)
        self.launcher.window.set_handler('on_key_press', self.on_key_press)
        self.launcher.window.set_handler('on_mouse_motion', self.on_mouse_motion)

    def unload_scene(self):
        self.launcher.window.remove_handlers()
        for record in self.records:
            pyglet.clock.unschedule(record.update)

    def launch_game(self):
        print(config.roms[abs(self.records[0].pos - 0)])
        subprocess.run([config.get_config()['mame_directory'] + 
                    config.get_config()['mame_executable'],
                    config.roms[abs(self.records[0].pos - 0)]],
                    cwd=config.get_config()['mame_directory'])

    def update_title(self):
        self.label_title.text = config.roms[abs(self.records[0].pos - 0)][
                        len(config.get_config()['roms_directory']):]

    def on_draw(self):
        self.launcher.window.clear()
        for record in self.records:
            record.draw()
        self.panel_top.draw()
        self.panel_left.draw()
        self.panel_right.draw()
        self.hint_left.draw()
        self.hint_right.draw()
        self.update_title()
        self.label_title.draw()
    
    def on_key_press(self, symbol, modifiers):
        if self.records[0].pos < 0:
            if symbol == config.bindings['right']:
                for record in self.records:
                    record.shift(50)
        if self.records[0].pos > 1 - len(self.records):
            if symbol == config.bindings['left']:
                for record in self.records:
                    record.shift(-50)
        if symbol == config.bindings['start']:
            self.launch_game()
        if symbol == config.bindings['settings'] :
            self.launcher.load_scene(OptionsMenu)

    def on_mouse_motion(self, x, y, dx, dy):
        if ((dx > 0 and self.records[0].pos < 0)
        or (dx < 0 and self.records[0].pos > 1 - len(self.records))):    
            for record in self.records:
                record.shift(dx * MOUSE_SENSITIVITY)