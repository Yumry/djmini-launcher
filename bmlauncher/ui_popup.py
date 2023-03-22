import bmlauncher.config as config
import pyglet
import pyglet.shapes as shapes
import bmlauncher.util as util

class UIPopUp(object):
    def __init__(self, text, font_size=config.get_config()['font_size']):
        self.popup_text = pyglet.text.Label(text, font_name='Arial',
                          font_size=font_size * util.SCALE_FACTOR,
                          x=util.scale_x(512),y=util.scale_y(384),
                          anchor_x='center', anchor_y='center')

        self.popup_bg = shapes.Rectangle(util.scale_x(512) - self.popup_text.content_width / 2 - 50, 
                        util.scale_y(300), self.popup_text.content_width + 100, 
                        util.scale_y(168), (41, 41, 41))
    def draw(self):
        self.popup_bg.draw()
        self.popup_text.draw()