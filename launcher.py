import pyglet
from pyglet.window import key
import bmlauncher.util as util
import bmlauncher.ui_shifted_row as ui_shifted_row

width = 1680
height = 1050

util.ui_scale = 0.4
window = pyglet.window.Window(width, height)

util.set_resolution(width, height)

records = []

for i in range(10):
    record_image = pyglet.resource.image('assets/record.png')
    newrecord = ui_shifted_row.UiShiftedRow(i, True, record_image, x = 512, y = 384)
    records.append(newrecord)

@window.event
def on_draw():
    window.clear()
    for record in records:
        record.draw()


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