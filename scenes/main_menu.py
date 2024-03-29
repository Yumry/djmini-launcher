import pyglet
from pyglet.window import key
import bmlauncher.util as util
import bmlauncher.ui_scrollable_row as ui_scrollable_row
from bmlauncher.ui_element import UIElement
from bmlauncher.ui_popup import UIPopUp
import bmlauncher.config as config
from scenes.scene import Scene
from scenes.options_menu import OptionsMenu
import subprocess
import threading

MOUSE_SENSITIVITY = config.get_config()['mouse_sensitivity']

class MainMenu(Scene):
    def start_scene(self):
        self.panel_top = UIElement(util.get_centered_image('assets/panel_top.png'),
                            x=512, y=720)

        self.panel_left = UIElement(util.get_centered_image('assets/panel_corner.png'), 
                            x=100, y=50)

        self.panel_right = UIElement(util.get_centered_image('assets/panel_corner.png'), 
                            x=924, y=50)
        self.panel_right.image = self.panel_right.image.get_transform(flip_x = True)

        self.hint_left = UIElement(util.get_centered_image('assets/hint_changegame.png'), 
                            x=80, y=50)

        self.hint_right = UIElement(util.get_centered_image('assets/hint_startgame.png'), 
                            x=944, y=50)

        self.loading_popup = UIPopUp('Loading...')

        self.records = []

        record_image = util.get_centered_image('assets/record.png')
        for i in range(len(config.roms)):
            newrecord = ui_scrollable_row.UiScrollableRow(
                i, True, record_image, x=512, y=360)
            self.records.append(newrecord)

        self.label_title = pyglet.text.Label('No ROMs found!',
                                font_name='Arial',
                                font_size=config.get_config()['font_size'] * util.SCALE_FACTOR,
                                x=util.scale_x(512), y = util.scale_y(550),
                                anchor_x='center', anchor_y='center')

        for record in self.records:
            pyglet.clock.schedule_interval(record.update, 0.0001)

        self.launcher.window.set_handler('on_draw', self.on_draw)
        self.launcher.window.set_handler('on_key_press', self.on_key_press)
        self.launcher.window.set_handler('on_mouse_motion', self.on_mouse_motion)
        if self.launcher.controller is not None:
            self.launcher.controller.set_handler('on_button_press', self.on_button_press)
            self.launcher.controller.set_handler('on_dpad_motion', self.on_dpad_motion)
            self.launcher.controller.set_handler('on_button_release', self.on_button_release)

        if self.launcher.native_controller is not None:
            self.launcher.native_controller.add_press_handler(self.on_native_button_press)
            self.launcher.native_controller.add_release_handler(self.on_native_button_release)
        
        self.active_buttons = []
        self.mame_subprocess = None
        self.input_enabled = True

        self.rom_list = []
        for rom_name in config.roms:
            rom_name = rom_name[len(config.get_config()['roms_directory']) + 1:-4]
            if rom_name in config.get_config()['rom_name_overrides']:
                rom_name = config.get_config()['rom_name_overrides'][rom_name]
            self.rom_list.append(rom_name)

    def unload_scene(self):
        self.launcher.window.remove_handlers()
        if self.launcher.controller is not None:
            self.launcher.controller.remove_handlers()
            self.launcher.controller.remove_handler('on_button_release', self.on_button_release)

        if self.launcher.native_controller is not None:
            self.launcher.native_controller.remove_handlers()

        for record in self.records:
            pyglet.clock.unschedule(record.update)

    def update_title(self):
        try:
            rom_name = self.rom_list[abs(self.records[0].pos - 0)]
            self.label_title.text = rom_name
        except:
            pass

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
        if not self.input_enabled:
            self.loading_popup.draw()

    def launch_mame(self):
        def run_mame_process():
            rom = ''
            command = [config.get_config()['mame_directory'] + '/' +
                       config.get_config()['mame_executable']]
            try:
                rom = config.roms[abs(self.records[0].pos - 0)]
                print(rom)
                command.append(rom)
                command += config.get_config()['mame_args'].split()
            except:
                print('No ROM found')
            
            try:
                self.mame_subprocess = subprocess.Popen(command,
                        cwd=config.get_config()['mame_directory'])
                self.mame_subprocess.wait()
                self.input_enabled = True
                self.launcher.lights_forwarder.connected = False
            except:
                self.input_enabled = True
                print('Unable to start mame!')
                self.launcher.lights_forwarder.connected = False

        self.input_enabled = False
        thread = threading.Thread(target=run_mame_process)
        thread.start()

    def close_mame(self):
        """The binding for this functions differently than the others.
            Rather than acting as an OR gate it acts as an
            AND gate, requiring ALL buttons under the binding
            to be pressed in order to close mame, where this function
            is then called."""
        close_bindings = config.bindings['close_mame']
        number_pressed = 0
        if close_bindings is not None:
            for btn in close_bindings:
                if btn in self.active_buttons:
                    number_pressed += 1
            print(number_pressed)
            if number_pressed == len(close_bindings):
                # All buttons under the binding are held. Close mame!
                if self.mame_subprocess is not None:
                    print('Closing mame!')
                    self.mame_subprocess.kill()
                    self.mame_subprocess = None
                    self.input_enabled = True

    def on_input(self, symbol):
        if self.input_enabled:
            try:
                if self.records[0].pos < 0:
                    if symbol in config.bindings['right']:
                        for record in self.records:
                            record.shift(2)
                if self.records[0].pos > 1 - len(self.records):
                    if symbol in config.bindings['left']:
                        for record in self.records:
                            record.shift(-2)
            except:
                pass
            if symbol in config.bindings['start']:
                self.launch_mame()
            if symbol in config.bindings['settings']:
                self.launcher.unload_scene()
                self.launcher.load_scene(OptionsMenu)
        if symbol in config.bindings['close_mame']:
            self.close_mame()

    def on_key_press(self, symbol, modifiers):
        self.on_input(symbol)

    def on_button_press(self, controller, pressed_button):
        button = 'btn_' + pressed_button
        self.active_buttons.append(button)
        self.on_input(button)
    
    def on_button_release(self, controller, released_button):
        button = 'btn_' + released_button
        if button in self.active_buttons:
            self.active_buttons.remove(button)

    def on_dpad_motion(self, controller, left, right, up, down):
        if left:
            self.on_input('dpad_l')
        if right:
            self.on_input('dpad_r')
        if up:
            self.on_input('dpad_u')
        if down:
            self.on_input('dpad_d')

    def on_mouse_motion(self, x, y, dx, dy):
        if self.input_enabled:
            try:
                if ((dx > 0 and self.records[0].pos < 0)
                or (dx < 0 and self.records[0].pos > 1 - len(self.records))):    
                    for record in self.records:
                        record.shift(dx * MOUSE_SENSITIVITY)
            except:
                pass

    def on_native_button_press(self, pressed_button):
        self.active_buttons.append(pressed_button)
        self.on_input(pressed_button)

    def on_native_button_release(self, released_button):
        if released_button in self.active_buttons:
            self.active_buttons.remove(released_button)