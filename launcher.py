import pyglet
from pyglet.window import key
import bmlauncher.util as util
import bmlauncher.ui_scrollable_row as ui_scrollable_row
import bmlauncher.ui_element as ui_element

width = 1680
height = 1050

util.ui_scale = 0.4
window = pyglet.window.Window(width, height)

util.set_resolution(width, height)


# Set up the UI

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

for i in range(10):
    record_image = pyglet.resource.image('assets/record.png')
    newrecord = ui_scrollable_row.UiScrollableRow(
        i, True, record_image, x=512, y=360)
    records.append(newrecord)

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


@window.event
def on_key_press(symbol, modifiers):
    if(records[0].pos < 0):
        if(symbol == key.RIGHT):
            for record in records:
                record.shift(30)
    if(records[0].pos > 1 - len(records)):
        if(symbol == key.LEFT):
            for record in records:
                record.shift(-30)


for record in records:
    pyglet.clock.schedule_interval(record.update, 0.00005)

pyglet.app.run()