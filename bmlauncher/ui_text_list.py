import pyglet
from pyglet import shapes
import pyglet.window.key as key
import bmlauncher.util as util
from enum import Enum
import bmlauncher.config as config
class Action(Enum):
    LABEL = 0
    CATEGORY = 1
    BACK = 2
    KEYBIND = 3
    JOYBIND = 4

class UITextListEntry(object):
    def __init__(self, label, action=Action.LABEL, input=None):
        self.label = label
        self.action = action
        self.input = input
        self.display_name = None
        if action == Action.KEYBIND:
            self.display_name = label.text

class UITextList(object):
    def __init__(self, x, y, width):
        self.entries = []
        key.EXCLAMATION
        self.x = x
        self.y = y
        self.selected = 0
        self.rect_selection = shapes.Rectangle(self.x, self.y, width, 0, (95, 62, 158))

    def append_entry(self, text, action=Action.LABEL, input=None):
        size = config.get_config()['font_size'] * util.SCALE_FACTOR
        new_label = pyglet.text.Label(text, font_name = 'Arial',
        font_size = size, x = self.x, y = self.y - (len(self.entries) * size * 1.4))
        
        if action == Action.CATEGORY:
            new_label.italic = True
            new_label.bold = True

        entry = UITextListEntry(new_label, action, input)
        self.entries.append(entry)
    
    def set_selection(self, selection_num):
        if selection_num in range(0, len(self.entries)):
            self.selected = selection_num

    def get_selection(self):
        return self.entries[self.selected]

    def draw(self):
        for i, entry in enumerate(self.entries):
            if i == self.selected:
                self.rect_selection.x = entry.label.x
                self.rect_selection.y = entry.label.y - util.scale_y(7)
                self.rect_selection.height = entry.label.content_height - 10
                self.rect_selection.draw()
            if entry.action == Action.KEYBIND:
                entry.label.text = entry.display_name + key.symbol_string(config.bindings[entry.input])
            entry.label.draw()