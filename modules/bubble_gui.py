import sys, os
sys.path.insert(0, os.path.abspath('..'))

from common.gfxutil import CLabelRect
from kivy.graphics import Color, Line, Rectangle
from kivy.graphics.instructions import InstructionGroup
from kivy.core.image import Image

class TimbreSelect(InstructionGroup):
    """
    Submodule to select the timbre of PhysicsBubble.
    """
    def __init__(self, pos, callback):
        super(TimbreSelect, self).__init__()

        self.selected = 'sine' # the actual important variable: which timbre is selected!

        # callback is needed to update PhysicsBubbleHandler's state for timbre
        self.callback = callback

        self.pos = pos
        self.margin = 20
        self.button_length = 64
        self.title_height = 50 # height of the word 'timbre'
        self.size = (
            (4 * self.button_length) + (5 * self.margin),
            self.button_length + (2 * self.margin) + self.title_height
        )

        self.white = (239/255, 226/255, 222/255)
        self.red = (201/255, 108/255, 130/255)

        self.border_color = Color(1, 0, 0)
        self.border = Line(rectangle=(*self.pos, *self.size))
        self.add(self.border_color)
        self.add(self.border)

        button_size = (self.button_length, self.button_length)
        self.timbres = {
            'sine': Rectangle(size=button_size, texture=Image('images/sine.png').texture),
            'square': Rectangle(size=button_size, texture=Image('images/square.png').texture),
            'triangle': Rectangle(size=button_size, texture=Image('images/triangle.png').texture),
            'sawtooth': Rectangle(size=button_size, texture=Image('images/sawtooth.png').texture)
        }
        self.timbre_bgs = {
            'sine': Rectangle(size=button_size),
            'square': Rectangle(size=button_size),
            'triangle': Rectangle(size=button_size),
            'sawtooth': Rectangle(size=button_size)
        }
        self.timbre_colors = {
            'sine': Color(*self.red), # default selected timbre
            'square': Color(*self.white),
            'triangle': Color(*self.white),
            'sawtooth': Color(*self.white)
        }

        x, y = self.pos

        sine_pos = (x + self.margin, y + self.margin)
        square_pos = (x + 2*self.margin + self.button_length, y + self.margin)
        triangle_pos = (x + 3*self.margin + 2*self.button_length, y + self.margin)
        sawtooth_pos = (x + 4*self.margin + 3*self.button_length, y + self.margin)

        for timbre, timbre_pos in zip(
            ('sine', 'square', 'triangle', 'sawtooth'),
            (sine_pos, square_pos, triangle_pos, sawtooth_pos)
        ):
            self.timbres[timbre].pos = self.timbre_bgs[timbre].pos = timbre_pos
            self.add(self.timbre_colors[timbre])
            self.add(self.timbre_bgs[timbre])
            self.add(self.timbres[timbre])

        title_pos = (x + self.size[0]/2, y + self.size[1] - self.title_height/2 - self.margin/2)
        self.title = CLabelRect(cpos=title_pos, text='timbre', font_size='18')
        self.add(Color(*self.white))
        self.add(self.title)

    def in_bounds(self, mouse_pos, obj_pos, obj_size):
        """
        Check if a mouse's position is inside an object.
        :param mouse_pos: (x, y) mouse position
        :param obj_pos: (x, y) object position
        :param obj_size: (width, height) object size
        """
        return (mouse_pos[0] >= obj_pos[0]) and \
               (mouse_pos[0] <= obj_pos[0] + obj_size[0]) and \
               (mouse_pos[1] >= obj_pos[1]) and \
               (mouse_pos[1] <= obj_pos[1] + obj_size[1])

    def on_touch_down(self, pos):
        button_size = (self.button_length, self.button_length)

        if self.in_bounds(pos, self.timbres['sine'].pos, button_size):
            self.select('sine')
            self.callback(self.selected)

        if self.in_bounds(pos, self.timbres['square'].pos, button_size):
            self.select('square')
            self.callback(self.selected)

        if self.in_bounds(pos, self.timbres['triangle'].pos, button_size):
            self.select('triangle')
            self.callback(self.selected)

        if self.in_bounds(pos, self.timbres['sawtooth'].pos, button_size):
            self.select('sawtooth')
            self.callback(self.selected)

    def select(self, timbre):
        self.timbre_colors[timbre].rgb = self.red
        self.selected = timbre
        others = [c for c in ['sine', 'square', 'triangle', 'sawtooth'] if c != timbre]
        for o in others:
            self.timbre_colors[o].rgb = self.white
