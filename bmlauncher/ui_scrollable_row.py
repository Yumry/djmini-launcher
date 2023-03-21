import random
from . import util
from . import ui_element

def snapto(x, base=10):
    return int(base * round(x / base))

class UiScrollableRow(ui_element.UIElement):
    def __init__(self, position, random_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos = position
        self.shiftby = 0
        self.shiftamount = 0
        self.x = self.width * self.pos + util.scale_x(512)
        if random_color:
            self.color = (random.randrange(150, 255), random.randrange(
                150, 255), random.randrange(150, 255))

    def update(self, dt):
        # First we check if we can shift this turn without misaligning.
        if(abs((self.shiftamount + self.shiftby) - 0) < self.width):
            self.x += self.shiftby
            self.shiftamount += self.shiftby
        else:
            # we can't move anymore without misaligning, so snap to the grid and save
            # our place in the lineup.
            self.x = snapto(self.x, self.width)
            self.shiftby = 0
            self.shiftamount = 0
            self.pos = int(snapto(self.x, self.width) / self.width) -1

    def shift(self, amount):
        self.shiftby = amount * util.SCALE_FACTOR