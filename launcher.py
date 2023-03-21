import pyglet
from pyglet.window import key
import bmlauncher.util as util
import bmlauncher.ui_scrollable_row as ui_scrollable_row
import bmlauncher.ui_element as ui_element
import bmlauncher.config as config
import subprocess

WIDTH = config.get_config()['resolution_x']
HEIGHT = config.get_config()['resolution_y']

MOUSE_SENSITIVITY = config.get_config()['mouse_sensitivity']

# load the config and initialize
config.initialize()

# Start up the window

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_exclusive_mouse(True)

panel_top = ui_element.UIElement(
    pyglet.resource.image('assets/panel_top.png'), x=512, y=720)

panel_left = ui_element.UIElement(
    pyglet.resource.image('assets/panel_corner.png'), x = 100, y = 50)

panel_right = ui_element.UIElement(
    pyglet.resource.image('assets/panel_corner.png'), x = 924, y = 50)
panel_right.image = panel_right.image.get_transform(flip_x = True)

hint_left = ui_element.UIElement(
    pyglet.resource.image('assets/hint_changegame.png'), x = 80, y = 50)
    
hint_right = ui_element.UIElement(
    pyglet.resource.image('assets/hint_startgame.png'), x = 944, y = 50)

records = []

for i in range(len(config.roms)):
    record_image = pyglet.resource.image('assets/record.png')
    newrecord = ui_scrollable_row.UiScrollableRow(
        i, True, record_image, x=512, y=360)
    records.append(newrecord)

label_title = pyglet.text.Label('Unknown ROM',
                                font_name='Arial',
                                font_size=50 * util.SCALE_FACTOR,
                                x=util.scale_x(512), y = util.scale_y(550),
                                anchor_x='center', anchor_y='center')

def launch_game():
    print(config.roms[abs(records[0].pos - 0)])
    subprocess.run([config.get_config()['mame_directory'] + 
                config.get_config()['mame_executable'],
                config.roms[abs(records[0].pos - 0)]],
                cwd=config.get_config()['mame_directory'])

def update_title():
    label_title.text = config.roms[abs(records[0].pos - 0)][
                       len(config.get_config()['roms_directory']):]

@window.event
def on_draw():
    window.clear()
    for record in records:
        record.draw()
    panel_top.draw()
    panel_left.draw()
    panel_right.draw()
    hint_left.draw()
    hint_right.draw()
    label_title.draw()
    update_title()


@window.event
def on_key_press(symbol, modifiers):
    if(records[0].pos < 0):
        if(symbol == key.RIGHT):
            for record in records:
                record.shift(50)
    if(records[0].pos > 1 - len(records)):
        if(symbol == key.LEFT):
            for record in records:
                record.shift(-50)
    if(symbol == key.ENTER):
        launch_game()

@window.event
def on_mouse_motion(x, y, dx, dy):
    if(dx > 0 and records[0].pos < 0):    
        for record in records:
            record.shift(dx * MOUSE_SENSITIVITY)
    if(dx < 0 and records[0].pos > 1 - len(records)):
        for record in records:
            record.shift(dx * MOUSE_SENSITIVITY * util.SCALE_FACTOR)

for record in records:
    pyglet.clock.schedule_interval(record.update, 0.00005)

update_title()
pyglet.app.run()