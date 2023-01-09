import pyglet
from . import util


class UIElement(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = util.SCALE_FACTOR
        util.center_image(self.image)
        self.x = (util.scale_x(self.x))
        self.y = (util.scale_y(self.y))

    def set_virtual_x(self, x):
        self.x = util.scale_x(x)

    def set_virtual_y(self, y):
        self.y = util.scale_y(y)
